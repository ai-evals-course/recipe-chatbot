#!/usr/bin/env python3
"""Run full evaluation using the LLM judge and judgy for corrected metrics.

This script runs the finalized judge on all traces and uses judgy to compute
the corrected success rate with confidence intervals.
"""

import os
import pandas as pd
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple, Final
from rich.console import Console
from rich.progress import track
import litellm
from judgy import estimate_success_rate
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
load_dotenv()

console = Console()

# Model used for the LLM judge
MODEL_NAME_JUDGE: Final[str] = os.environ.get("MODEL_NAME_JUDGE", "gpt-4o-nano")

MAX_WORKERS = 32

def load_traces(csv_path: str) -> List[Dict[str, Any]]:
    """Load traces from CSV file."""
    df = pd.read_csv(csv_path)
    return df.to_dict('records')

def load_judge_prompt(prompt_path: str) -> str:
    """Load the judge prompt from file."""
    with open(prompt_path, 'r') as f:
        return f.read()

def load_test_data(judgy_path: str) -> Tuple[List[int], List[int]]:
    """Load test labels and predictions for judgy."""
    with open(judgy_path, 'r') as f:
        data = json.load(f)
    return data["test_labels"], data["test_preds"]

def evaluate_single_trace_for_binary(args: tuple) -> int:
    """Evaluate a single trace and return binary prediction (1 for PASS, 0 for FAIL)."""
    trace, judge_prompt = args
    
    query = trace["query"]
    dietary_restriction = trace["dietary_restriction"]
    response = trace["response"]
    
    # Format the prompt using string replacement
    formatted_prompt = judge_prompt.replace("__QUERY__", query)
    formatted_prompt = formatted_prompt.replace("__DIETARY_RESTRICTION__", dietary_restriction)
    formatted_prompt = formatted_prompt.replace("__RESPONSE__", response)
    
    try:
        # Get judge prediction
        completion = litellm.completion(
            model=MODEL_NAME_JUDGE,
            messages=[{"role": "user", "content": formatted_prompt}],
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        # Parse JSON response
        try:
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "{" in response_text and "}" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_text = response_text[json_start:json_end]
            else:
                json_text = response_text
            
            result = json.loads(json_text)
            predicted_label = result.get("label", "UNKNOWN")
            
            # Convert to binary: 1 for PASS, 0 for FAIL
            if predicted_label == "PASS":
                return 1
            elif predicted_label == "FAIL":
                return 0
            else:
                # Default to FAIL for unknown/error cases
                return 0
                
        except json.JSONDecodeError:
            # Default to FAIL for parsing errors
            return 0
            
    except Exception as e:
        # Default to FAIL for API errors
        return 0

def run_judge_on_traces(judge_prompt: str, traces: List[Dict[str, Any]], 
                       max_workers: int = MAX_WORKERS) -> List[int]:
    """Run the judge on all traces and return binary predictions using parallel processing."""
    
    console.print(f"[yellow]Running judge on {len(traces)} traces with {max_workers} workers...")
    
    # Prepare tasks for parallel processing
    tasks = [(trace, judge_prompt) for trace in traces]
    
    predictions = []
    
    # Use ThreadPoolExecutor for parallel evaluation
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_task = {executor.submit(evaluate_single_trace_for_binary, task): task for task in tasks}
        
        # Process completed tasks with progress tracking
        with console.status("[yellow]Evaluating traces in parallel...") as status:
            completed = 0
            total = len(tasks)
            
            for future in as_completed(future_to_task):
                result = future.result()
                predictions.append(result)
                completed += 1
                
                status.update(f"[yellow]Evaluated {completed}/{total} traces ({completed/total*100:.1f}%)")
    
    console.print(f"[green]Completed parallel evaluation of {len(predictions)} traces")
    return predictions

def compute_metrics_with_judgy(test_labels: List[int], test_preds: List[int], 
                              unlabeled_preds: List[int]) -> Tuple[float, float, float, float]:
    """Compute corrected success rate and confidence interval using judgy."""
    
    # Estimate true success rate with judgy
    theta_hat, lower_bound, upper_bound = estimate_success_rate(
        test_labels=test_labels,
        test_preds=test_preds,
        unlabeled_preds=unlabeled_preds
    )
    
    # Also compute raw observed success rate
    raw_success_rate = np.mean(unlabeled_preds)
    
    return theta_hat, lower_bound, upper_bound, raw_success_rate

def save_final_results(theta_hat: float, lower_bound: float, upper_bound: float, 
                      raw_success_rate: float, total_traces: int, 
                      results_dir: Path) -> None:
    """Save final evaluation results."""
    
    results = {
        "final_evaluation": {
            "total_traces_evaluated": total_traces,
            "raw_observed_success_rate": raw_success_rate,
            "corrected_success_rate": theta_hat,
            "confidence_interval_95": {
                "lower_bound": lower_bound,
                "upper_bound": upper_bound
            },
            "interpretation": {
                "description": "Corrected success rate accounts for judge errors (TPR/TNR)",
                "raw_vs_corrected": f"Raw rate: {raw_success_rate:.3f}, Corrected rate: {theta_hat:.3f}"
            }
        }
    }
    
    results_path = results_dir / "final_evaluation.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    console.print(f"[green]Saved final results to {results_path}")

def print_interpretation(theta_hat: float, lower_bound: float, upper_bound: float, 
                        raw_success_rate: float) -> None:
    """Print interpretation of results."""
    
    console.print("\n[bold]Final Results:")
    console.print("=" * 30)
    
    console.print(f"[blue]Raw Observed Success Rate: {raw_success_rate:.3f} ({raw_success_rate*100:.1f}%)")
    console.print(f"[green]Corrected Success Rate: {theta_hat:.3f} ({theta_hat*100:.1f}%)")
    console.print(f"[yellow]95% Confidence Interval: [{lower_bound:.3f}, {upper_bound:.3f}]")
    console.print(f"[yellow]                        [{lower_bound*100:.1f}%, {upper_bound*100:.1f}%]")
    
    correction_magnitude = abs(raw_success_rate - theta_hat)
    console.print(f"[cyan]Correction Applied: {correction_magnitude:.3f} ({correction_magnitude*100:.1f} percentage points)")

def main():
    """Main function for full evaluation."""
    console.print("[bold blue]Full Recipe Bot Dietary Adherence Evaluation")
    console.print("=" * 60)
    
    # Set up paths
    script_dir = Path(__file__).parent
    hw3_dir = script_dir.parent
    data_dir = hw3_dir / "data"
    results_dir = hw3_dir / "results"
    
    # Load judge prompt
    prompt_path = results_dir / "judge_prompt.txt"
    if not prompt_path.exists():
        console.print("[red]Error: Judge prompt not found!")
        console.print("[yellow]Please run develop_judge.py first.")
        return
    
    judge_prompt = load_judge_prompt(str(prompt_path))
    console.print("[green]Loaded judge prompt")
    
    # Load test set performance data for judgy
    judgy_path = results_dir / "judgy_test_data.json"
    if not judgy_path.exists():
        console.print("[red]Error: Test set performance data not found!")
        console.print("[yellow]Please run evaluate_judge.py first.")
        return
    
    test_labels, test_preds = load_test_data(str(judgy_path))
    console.print(f"[green]Loaded test set performance: {len(test_labels)} examples")
    
    # Load all raw traces for evaluation
    traces_path = data_dir / "raw_traces.csv"
    if not traces_path.exists():
        console.print("[red]Error: Raw traces not found!")
        console.print("[yellow]Please run generate_traces.py first.")
        return
    
    all_traces = load_traces(str(traces_path))
    console.print(f"[green]Loaded {len(all_traces)} traces for evaluation")
    
    # Run judge on all traces
    console.print("[yellow]Running judge on all traces... This will take a while.")
    predictions = run_judge_on_traces(judge_prompt, all_traces)
    
    console.print(f"[green]Completed evaluation of {len(predictions)} traces")
    console.print(f"[blue]Raw success rate: {np.mean(predictions):.3f}")
    
    # Compute corrected metrics with judgy
    console.print("[yellow]Computing corrected success rate with judgy...")
    theta_hat, lower_bound, upper_bound, raw_success_rate = compute_metrics_with_judgy(
        test_labels, test_preds, predictions
    )
    
    # Print and save results
    print_interpretation(theta_hat, lower_bound, upper_bound, raw_success_rate)
    save_final_results(theta_hat, lower_bound, upper_bound, raw_success_rate, 
                      len(all_traces), results_dir)
    
    console.print("\n[bold green]Full evaluation completed successfully!")
    console.print("[blue]Check the results/ directory for detailed outputs.")

if __name__ == "__main__":
    main() 