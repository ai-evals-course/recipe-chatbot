"""Bulk testing utility for the recipe chatbot agent.

Reads a CSV file containing user queries, fires them against the agent
concurrently, and stores the results for later manual evaluation.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path to allow absolute imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import datetime as dt
import json
from concurrent.futures import ThreadPoolExecutor

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from backend.utils import get_agent_response

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

DEFAULT_CSV: Path = Path("data/sample_queries.csv")
RESULTS_DIR: Path = Path("results")
MAX_WORKERS = 32


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def read_queries(csv_path: Path) -> list[dict[str, str]]:
    """Read queries from CSV (expects 'id' and 'query' columns)."""
    import csv
    
    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        queries = [row for row in reader if row.get("id") and row.get("query")]
    
    return queries


def process_query(query_id: str, query: str) -> tuple[str, str, str]:
    """Process a single query, returning (id, query, response)."""
    try:
        initial_messages = [{"role": "user", "content": query}]
        updated_history = get_agent_response(initial_messages)
        
        if updated_history and updated_history[-1]["role"] == "assistant":
            response = updated_history[-1]["content"]
        else:
            response = "Error: No assistant reply found"
            
        return query_id, query, response
        
    except Exception as e:
        return query_id, query, f"Error: {e!r}"


def print_result(console: Console, index: int, total: int, query_id: str, query: str, response: str) -> None:
    """Print a formatted result panel."""
    panel_content = Text()
    panel_content.append(f"ID: {query_id}\n", style="bold magenta")
    panel_content.append("Query:\n", style="bold yellow")
    panel_content.append(f"{query}\n\n")
    
    panel_group = Group(panel_content, Markdown("--- Response ---"), Markdown(response))
    
    console.print(Panel(
        panel_group,
        title=f"Result {index + 1}/{total} - ID: {query_id}",
        border_style="cyan"
    ))


def write_results(output_path: Path, results: list[tuple[str, str, str]]) -> None:
    """Write results to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    json_data = [
        {"id": result[0], "query": result[1], "response": result[2]}
        for result in results
    ]
    
    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=2, ensure_ascii=False)


# -----------------------------------------------------------------------------
# Main logic
# -----------------------------------------------------------------------------

def run_bulk_test(csv_path: Path, num_workers: int = MAX_WORKERS) -> None:
    """Execute bulk testing of queries from CSV file."""
    console = Console()
    
    queries = read_queries(csv_path)
    actual_workers = min(num_workers, len(queries))
    
    console.print(f"[bold blue]Processing {len(queries)} queries with {actual_workers} workers...[/bold blue]")
    
    with ThreadPoolExecutor(max_workers=actual_workers) as executor:
        results = list(executor.map(
            lambda item: process_query(item["id"], item["query"]),
            queries
        ))
    
    for i, (query_id, query, response) in enumerate(results):
        print_result(console, i, len(results), query_id, query, response)
    
    console.print("[bold blue]All queries processed.[/bold blue]")
    
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = RESULTS_DIR / f"results_{timestamp}.json"
    
    write_results(output_path, results)
    
    console.print(f"[bold green]Saved {len(results)} results to {output_path}[/bold green]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk test the recipe chatbot")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help="Path to CSV file containing queries (columns: 'id', 'query')"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=MAX_WORKERS,
        help=f"Number of worker threads (default: {MAX_WORKERS})"
    )
    args = parser.parse_args()
    
    run_bulk_test(args.csv, args.workers)
