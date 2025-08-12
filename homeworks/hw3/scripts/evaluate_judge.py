#!/usr/bin/env python3
"""Evaluate the LLM judge performance on the test set.

This script evaluates the finalized LLM judge on the test set to get
unbiased estimates of TPR and TNR for use with judgy.
"""

import os
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Final
from rich.console import Console
from rich.progress import track
import litellm
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv
load_dotenv()

MAX_WORKERS = 32

console = Console()

# Model used for the LLM judge
MODEL_NAME_JUDGE: Final[str] = os.environ.get("MODEL_NAME_JUDGE", "gpt-4o-nano")

def load_data_split(csv_path: str) -> List[Dict[str, Any]]:
    """Load a data split from CSV file."""
    df = pd.read_csv(csv_path)
    return df.to_dict('records')

def load_judge_prompt(prompt_path: str) -> str:
    """Load the judge prompt from file."""
    with open(prompt_path, 'r') as f:
        return f.read()

def evaluate_single_trace(args: tuple) -> Dict[str, Any]:
    """Evaluate a single trace with the judge - for parallel processing."""
    trace, judge_prompt = args
    
    query = trace["query"]
    dietary_restriction = trace["dietary_restriction"]
    response = trace["response"]
    true_label = trace["label"]
    
    # Format the prompt using string replacement
    formatted_prompt = judge_prompt.replace("__QUERY__", query)
    formatted_prompt = formatted_prompt.replace("__DIETARY_RESTRICTION__", dietary_restriction)
    formatted_prompt = formatted_prompt.replace("__RESPONSE__", response)
    
    try:
        # Get judge prediction
        completion = litellm.completion(
            model=MODEL_NAME_JUDGE,  # Use the same model as in development
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
            reasoning = result.get("reasoning", "")
        except json.JSONDecodeError:
            predicted_label = "UNKNOWN"
            reasoning = "Failed to parse JSON response"
        
        return {
            "trace_id": trace.get("trace_id", "unknown"),
            "query": query,
            "dietary_restriction": dietary_restriction,
            "response": response[:200] + "..." if len(response) > 200 else response,
            "true_label": true_label,
            "predicted_label": predicted_label,
            "reasoning": reasoning,
            "success": True
        }
        
    except Exception as e:
        return {
            "trace_id": trace.get("trace_id", "unknown"),
            "query": query,
            "dietary_restriction": dietary_restriction,
            "response": response[:200] + "..." if len(response) > 200 else response,
            "true_label": true_label,
            "predicted_label": "ERROR",
            "reasoning": f"Error: {str(e)}",
            "success": False
        }

def evaluate_judge_on_test(judge_prompt: str, test_traces: List[Dict[str, Any]], 
                          max_workers: int = MAX_WORKERS) -> Tuple[float, float, List[Dict[str, Any]]]:
    """Evaluate the judge prompt on the test set using parallel processing."""
    
    console.print(f"[yellow]Evaluating judge on {len(test_traces)} test traces with {max_workers} workers...")
    
    # Prepare tasks for parallel processing
    tasks = [(trace, judge_prompt) for trace in test_traces]
    
    predictions = []
    
    # Use ThreadPoolExecutor for parallel evaluation
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_task = {executor.submit(evaluate_single_trace, task): task for task in tasks}
        
        # Process completed tasks with progress tracking
        with console.status("[yellow]Evaluating traces in parallel...") as status:
            completed = 0
            total = len(tasks)
            
            for future in as_completed(future_to_task):
                result = future.result()
                predictions.append(result)
                completed += 1
                
                if not result["success"]:
                    console.print(f"[yellow]Warning: Failed to evaluate trace {result['trace_id']}: {result.get('reasoning', 'Unknown error')}")
                
                status.update(f"[yellow]Evaluated {completed}/{total} traces ({completed/total*100:.1f}%)")
    
    console.print(f"[green]Completed parallel evaluation of {len(predictions)} traces")
    
    # Calculate TPR and TNR
    tp = sum(1 for p in predictions if p["true_label"] == "PASS" and p["predicted_label"] == "PASS")
    fn = sum(1 for p in predictions if p["true_label"] == "PASS" and p["predicted_label"] == "FAIL")
    tn = sum(1 for p in predictions if p["true_label"] == "FAIL" and p["predicted_label"] == "FAIL")
    fp = sum(1 for p in predictions if p["true_label"] == "FAIL" and p["predicted_label"] == "PASS")
    
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    tnr = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    
    return tpr, tnr, predictions

def analyze_errors(predictions: List[Dict[str, Any]]) -> None:
    """Analyze prediction errors to understand judge performance."""
    
    # False positives (predicted PASS but actually FAIL)
    false_positives = [p for p in predictions if p["true_label"] == "FAIL" and p["predicted_label"] == "PASS"]
    
    # False negatives (predicted FAIL but actually PASS)
    false_negatives = [p for p in predictions if p["true_label"] == "PASS" and p["predicted_label"] == "FAIL"]
    
    console.print(f"\n[bold]Error Analysis:")
    console.print(f"False Positives: {len(false_positives)}")
    console.print(f"False Negatives: {len(false_negatives)}")
    
    if false_positives:
        console.print(f"\n[red]Sample False Positives (Judge said PASS, should be FAIL):")
        for i, fp in enumerate(false_positives[:3], 1):
            console.print(f"{i}. {fp['dietary_restriction']}: {fp['query']}")
            console.print(f"   Reasoning: {fp['reasoning'][:100]}...")
    
    if false_negatives:
        console.print(f"\n[yellow]Sample False Negatives (Judge said FAIL, should be PASS):")
        for i, fn in enumerate(false_negatives[:3], 1):
            console.print(f"{i}. {fn['dietary_restriction']}: {fn['query']}")
            console.print(f"   Reasoning: {fn['reasoning'][:100]}...")

def save_results(tpr: float, tnr: float, predictions: List[Dict[str, Any]], 
                results_dir: Path) -> None:
    """Save evaluation results."""
    
    # Save performance metrics
    performance = {
        "test_set_performance": {
            "true_positive_rate": tpr,
            "true_negative_rate": tnr,
            "balanced_accuracy": (tpr + tnr) / 2,
            "total_predictions": len(predictions),
            "correct_predictions": sum(1 for p in predictions if p["true_label"] == p["predicted_label"]),
            "accuracy": sum(1 for p in predictions if p["true_label"] == p["predicted_label"]) / len(predictions)
        }
    }
    
    performance_path = results_dir / "judge_performance.json"
    with open(performance_path, 'w') as f:
        json.dump(performance, f, indent=2)
    console.print(f"[green]Saved performance metrics to {performance_path}")
    
    # Save detailed predictions
    predictions_path = results_dir / "test_predictions.json"
    with open(predictions_path, 'w') as f:
        json.dump(predictions, f, indent=2)
    console.print(f"[green]Saved test predictions to {predictions_path}")
    
    # Save predictions in format for judgy
    test_labels = [1 if p["true_label"] == "PASS" else 0 for p in predictions]
    test_preds = [1 if p["predicted_label"] == "PASS" else 0 for p in predictions]
    
    judgy_data = {
        "test_labels": test_labels,
        "test_preds": test_preds,
        "description": "Test set labels and predictions for judgy evaluation"
    }
    
    judgy_path = results_dir / "judgy_test_data.json"
    with open(judgy_path, 'w') as f:
        json.dump(judgy_data, f, indent=2)
    console.print(f"[green]Saved judgy test data to {judgy_path}")

def main():
    """Main function to evaluate the judge on test set."""
    console.print("[bold blue]LLM Judge Test Set Evaluation")
    console.print("=" * 50)
    
    # Set up paths
    script_dir = Path(__file__).parent
    hw3_dir = script_dir.parent
    data_dir = hw3_dir / "data"
    results_dir = hw3_dir / "results"
    
    # Load test set
    test_path = data_dir / "test_set.csv"
    if not test_path.exists():
        console.print("[red]Error: Test set not found!")
        console.print("[yellow]Please run split_data.py first.")
        return
    
    test_traces = load_data_split(str(test_path))
    console.print(f"[green]Loaded {len(test_traces)} test traces")
    
    # Load judge prompt
    prompt_path = results_dir / "judge_prompt.txt"
    if not prompt_path.exists():
        console.print("[red]Error: Judge prompt not found!")
        console.print("[yellow]Please run develop_judge.py first.")
        return
    
    judge_prompt = load_judge_prompt(str(prompt_path))
    console.print("[green]Loaded judge prompt")
    
    # Evaluate judge on test set
    console.print("[yellow]Evaluating judge on test set... This may take a while.")
    tpr, tnr, predictions = evaluate_judge_on_test(judge_prompt, test_traces)
    
    # Print results
    console.print(f"\n[bold]Judge Performance on Test Set:")
    console.print(f"True Positive Rate (TPR): {tpr:.3f}")
    console.print(f"True Negative Rate (TNR): {tnr:.3f}")
    console.print(f"Balanced Accuracy: {(tpr + tnr) / 2:.3f}")
    console.print(f"Overall Accuracy: {sum(1 for p in predictions if p['true_label'] == p['predicted_label']) / len(predictions):.3f}")
    
    # Analyze errors
    analyze_errors(predictions)
    
    # Save results
    save_results(tpr, tnr, predictions, results_dir)
    
    console.print("\n[bold green]Test set evaluation completed!")
    console.print("[blue]Results saved for use with judgy in the final evaluation step.")

if __name__ == "__main__":
    main() 