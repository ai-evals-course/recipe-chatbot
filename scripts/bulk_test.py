from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path to allow a_s_b_absolute imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

"""Bulk testing utility for the recipe chatbot agent.

Reads a CSV file containing user queries, fires them against the `/chat`
endpoint concurrently, and stores the results for later manual evaluation.
"""

import argparse
import csv
import datetime as dt
import json
from typing import List, Tuple, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from backend.utils import get_agent_response, SYSTEM_PROMPT

# -----------------------------------------------------------------------------
# Configuration helpers
# -----------------------------------------------------------------------------

DEFAULT_CSV: Path = Path("data/sample_queries.csv")
RESULTS_DIR: Path = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

MAX_WORKERS = 32 # For ThreadPoolExecutor

# -----------------------------------------------------------------------------
# Core logic
# -----------------------------------------------------------------------------

# --- Sync function for ThreadPoolExecutor ---
def process_query_sync(
    item: Dict[str, str],
) -> Tuple[str, str, List[Dict[str, str]]]:
    """Processes a single query by calling the agent directly."""
    query_id = item["id"]
    initial_query = item["query"]
    messages: List[Dict[str, str]] = [{"role": "user", "content": initial_query}]
    try:
        # get_agent_response now returns the full history
        messages = get_agent_response(messages)

        i = 1
        while f"human_followup_{i}" in item and item[f"human_followup_{i}"]:
            followup_query = item[f"human_followup_{i}"]
            messages.append({"role": "user", "content": followup_query})
            messages = get_agent_response(messages)
            i += 1

        return query_id, initial_query, messages
    except Exception as e:
        error_message = f"Error processing query: {str(e)}"
        messages.append({"role": "system", "content": error_message})
        return query_id, initial_query, messages


# Renamed and made sync
def run_bulk_test(csv_path: Path, num_workers: int = MAX_WORKERS) -> None:
    """Main entry point for bulk testing (synchronous version)."""

    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        # Expects columns 'id' and 'query'
        input_data: List[Dict[str, str]] = [
            row for row in reader if row.get("id") and row.get("query")
        ]

    if not input_data:
        raise ValueError(
            "No valid data (with 'id' and 'query') found in the provided CSV file."
        )

    console = Console()
    results_data: List[
        Tuple[str, str, str]
    ] = []  # Will store (id, query, response)
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_data = {
            executor.submit(process_query_sync, item): item for item in input_data
        }
        console.print(
            f"[bold blue]Submitting {len(input_data)} queries to the executor...[/bold blue]"
        )
        for i, future in enumerate(as_completed(future_to_data)):
            item_data = future_to_data[future]
            item_id = item_data["id"]
            item_query = item_data["query"]
            try:
                processed_id, original_query, conversation_history = future.result()
                conversation_json = json.dumps(conversation_history)
                results_data.append(
                    (processed_id, original_query, conversation_json)
                )

                panel_content = Text()
                panel_content.append(f"ID: {processed_id}\n", style="bold magenta")

                conversation_group = []
                for msg in conversation_history:
                    role = msg.get("role")
                    content = msg.get("content", "")
                    if role == "user":
                        conversation_group.append(
                            Text("👤 User:", style="bold yellow")
                        )
                        conversation_group.append(Text(content))
                    elif role == "assistant":
                        conversation_group.append(
                            Text("🤖 Assistant:", style="bold green")
                        )
                        conversation_group.append(Markdown(content))
                    elif role == "system":  # for errors
                        conversation_group.append(
                            Text("🔧 System:", style="bold red")
                        )
                        conversation_group.append(Text(content))

                panel_group = Group(panel_content, Group(*conversation_group))

                console.print(
                    Panel(
                        panel_group,  # Pass the group as the single renderable
                        title=f"Result {i+1}/{len(input_data)} - ID: {processed_id}",
                        border_style="cyan",
                    )
                )

            except Exception as exc:
                console.print(
                    Panel(
                        f"[bold red]Exception for ID {item_id}, Query:[/bold red]\n{item_query}\n\n[bold red]Error:[/bold red]\n{exc}",
                        title=f"Error in Result {i+1}/{len(input_data)} - ID: {item_id}",
                        border_style="red",
                    )
                )
                error_history = [
                    {
                        "role": "system",
                        "content": f"Exception during processing: {str(exc)}",
                    }
                ]
                results_data.append(
                    (item_id, item_query, json.dumps(error_history))
                )
        console.print("[bold blue]All queries processed.[/bold blue]")

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = RESULTS_DIR / f"results_{timestamp}.csv"

    with out_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["id", "query", "conversation_history"])
        writer.writerows(results_data)

    console.print(
        f"[bold green]Saved {len(results_data)} results to {str(out_path)}[/bold green]"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk test the recipe chatbot")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help="Path to CSV file containing queries (column name: 'query').",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=MAX_WORKERS,
        help=f"Number of worker threads (default: {MAX_WORKERS}).",
    )
    args = parser.parse_args()
    run_bulk_test(args.csv, args.workers)
