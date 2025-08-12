#!/usr/bin/env python3
"""Develop and refine the LLM judge prompt for dietary adherence evaluation.

By default the script will use the base prompt provided by the course and add
one random positive and three random negative few-shot examples from the train
set.

This script also offers other possibilities to create the judge prompt. These 
other options can all be set in the global variables at the top of the file.

This opens the opportunity to first run the script with the default settings
which will result in the default prompt with random few-shot examples saved as
`/homeworks/hw3/results/judge_prompt.txt`. And then adjust this prompt manually
and run the script again with `OWN_PROMPT = True` to use your own manually
changed prompt.

This script offers two options for defining the base prompt:

- Use the base prompt profided by the course with automatically selected few-shot examples.
- Use a prompt of your own design with manually selected few-shot examples.

When using the base prompt profided by the course, this script offers two options for
adding the few-shot examples:

- Randomly add few-shot examples from the train set.
- Randomly add few-shot examples from the train set, but use a seed for reproducibility.

When using a prompt of your own design, be sure to:
- place it in `homeworks/hw3/results/judge_prompt.txt`,
- be sure to have the following placeholders in the prompt: 
  - `__QUERY__`, 
  - `__DIETARY_RESTRICTION__`, 
  - `__RESPONSE__`.
  The script uses these to embed the query, dietary restriction and recipe response in the
  evaluation prompt.
"""

import os
import json
import pandas as pd
import random
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Final
from rich.console import Console
import litellm
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global variables that can be set by user
SEED = None # Set to an integer to use a seed for reproducibility of selected few-shot examples
OWN_PROMPT = False # Set to True to use a base prompt of your own design

# Start script
load_dotenv()
MAX_WORKERS = 32

console = Console()

# Model used for the LLM judge
MODEL_NAME_JUDGE: Final[str] = os.environ.get("MODEL_NAME_JUDGE", "gpt-4o-nano")

def load_data_split(csv_path: str) -> List[Dict[str, Any]]:
    """Load a data split from CSV file."""
    df = pd.read_csv(csv_path)
    return df.to_dict('records')

def select_few_shot_examples(train_traces: List[Dict[str, Any]], 
                           num_positive: int = 1, 
                           num_negative: int = 3,
                           seed: Optional[int] = None) -> List[Dict[str, Any]]:
    """Select few-shot examples randomly from train set."""
    
    console.print("[yellow]Selecting random few-shot examples...")
    
    # Separate by label
    train_pass = [trace for trace in train_traces if trace["label"] == "PASS"]
    train_fail = [trace for trace in train_traces if trace["label"] == "FAIL"]
    
    selected_examples = []
    
    # Select positive examples (PASS) randomly
    if seed is not None:
        random.seed(seed)
    if train_pass and len(train_pass) >= num_positive:
        selected_examples.extend(random.sample(train_pass, num_positive))
    elif train_pass:
        selected_examples.extend(train_pass)  # Use all available if less than requested
    
    # Select negative examples (FAIL) randomly
    if train_fail and len(train_fail) >= num_negative:
        selected_examples.extend(random.sample(train_fail, num_negative))
    elif train_fail:
        selected_examples.extend(train_fail)  # Use all available if less than requested

    pass_c = len([e for e in selected_examples if e['label'] == 'PASS'])
    fail_c = len([e for e in selected_examples if e['label'] == 'FAIL'])
    console.print(
        f"[green]Selected {len(selected_examples)} "
        f"few-shot examples ({pass_c} PASS, {fail_c} FAIL)")
    return selected_examples

def create_judge_prompt(few_shot_examples: List[Dict[str, Any]]) -> str:
    """Create the LLM judge prompt with few-shot examples."""
    
    # Base prompt
    base_prompt = """You are an expert nutritionist and dietary specialist evaluating whether recipe responses properly adhere to specified dietary restrictions.

DIETARY RESTRICTION DEFINITIONS:
- Vegan: No animal products (meat, dairy, eggs, honey, etc.)
- Vegetarian: No meat or fish, but dairy and eggs are allowed
- Gluten-free: No wheat, barley, rye, or other gluten-containing grains
- Dairy-free: No milk, cheese, butter, yogurt, or other dairy products
- Keto: Very low carb (typically <20g net carbs), high fat, moderate protein
- Paleo: No grains, legumes, dairy, refined sugar, or processed foods
- Pescatarian: No meat except fish and seafood
- Kosher: Follows Jewish dietary laws (no pork, shellfish, mixing meat/dairy)
- Halal: Follows Islamic dietary laws (no pork, alcohol, proper slaughter)
- Nut-free: No tree nuts or peanuts
- Low-carb: Significantly reduced carbohydrates (typically <50g per day)
- Sugar-free: No added sugars or high-sugar ingredients
- Raw vegan: Vegan foods not heated above 118°F (48°C)
- Whole30: No grains, dairy, legumes, sugar, alcohol, or processed foods
- Diabetic-friendly: Low glycemic index, controlled carbohydrates
- Low-sodium: Reduced sodium content for heart health

EVALUATION CRITERIA:
- PASS: The recipe clearly adheres to the dietary preferences with appropriate ingredients and preparation methods
- FAIL: The recipe contains ingredients or methods that violate the dietary preferences
- Consider both explicit ingredients and cooking methods

Here are some examples of how to evaluate dietary adherence:

"""
    
    # Add few-shot examples
    for i, example in enumerate(few_shot_examples, 1):
        base_prompt += f"\nExample {i}:\n"
        base_prompt += f"Query: {example['query']}\n"
        base_prompt += f"Recipe Response: {example['response']}\n"
        base_prompt += f"Reasoning: {example['reasoning']}\n"
        base_prompt += f"Label: {example['label']}\n"
    
    # Add evaluation template - using placeholders that won't conflict with JSON
    base_prompt += """

Now evaluate the following recipe response:

Query: __QUERY__
Dietary Restriction: __DIETARY_RESTRICTION__
Recipe Response: __RESPONSE__

Provide your evaluation in the following JSON format:
{
    "reasoning": "Detailed explanation of your evaluation, citing specific ingredients or methods",
    "label": "PASS" or "FAIL"
}"""
    
    return base_prompt

def read_judge_prompt(f: Path # file path to the judge prompt
                     ) -> str:
    """Read the judge prompt from the file."""

    if not f.exists():
        raise FileNotFoundError(f"Judge prompt file {f} does not exist.")

    return f.read_text(encoding='utf-8')

def evaluate_single_trace(args: tuple) -> Dict[str, Any]:
    """Evaluate a single trace with the judge - for parallel processing."""
    trace, judge_prompt = args
    
    query = trace["query"]
    dietary_restriction = trace["dietary_restriction"]
    response = trace["response"]
    true_label = trace["label"]
    
    # Format the prompt using string replacement
    if not "__QUERY__" in judge_prompt:
        raise ValueError("Judge prompt does not contain __QUERY__ placeholder.")
    if not "__DIETARY_RESTRICTION__" in judge_prompt:
        raise ValueError("Judge prompt does not contain __DIETARY_RESTRICTION__ placeholder.")
    if not "__RESPONSE__" in judge_prompt:
        raise ValueError("Judge prompt does not contain __RESPONSE__ placeholder.")
    
    formatted_prompt = judge_prompt.replace("__QUERY__", query)
    formatted_prompt = formatted_prompt.replace("__DIETARY_RESTRICTION__", dietary_restriction)
    formatted_prompt = formatted_prompt.replace("__RESPONSE__", response)
    
    try:
        # Get judge prediction
        completion = litellm.completion(
            model=MODEL_NAME_JUDGE,  # Use a cheaper model for judge evaluation
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
        except json.JSONDecodeError:
            predicted_label = "UNKNOWN"
        
        return {
            "trace_id": trace.get("trace_id", "unknown"),
            "true_label": true_label,
            "predicted_label": predicted_label,
            "query": query,
            "dietary_restriction": dietary_restriction,
            "success": True
        }
        
    except Exception as e:
        return {
            "trace_id": trace.get("trace_id", "unknown"),
            "true_label": true_label,
            "predicted_label": "ERROR",
            "query": query,
            "dietary_restriction": dietary_restriction,
            "success": False,
            "error": str(e)
        }

def evaluate_judge_on_dev(judge_prompt: str, dev_traces: List[Dict[str, Any]], 
                         sample_size: int = 50, max_workers: int = MAX_WORKERS) -> Tuple[float, float, List[Dict[str, Any]]]:
    """Evaluate the judge prompt on a sample of the dev set using parallel processing."""
    
    # Sample dev traces for evaluation
    if len(dev_traces) > sample_size:
        sampled_traces = random.sample(dev_traces, sample_size)
    else:
        sampled_traces = dev_traces
    
    console.print(f"[yellow]Evaluating judge on {len(sampled_traces)} dev traces with {max_workers} workers...")
    
    # Prepare tasks for parallel processing
    tasks = [(trace, judge_prompt) for trace in sampled_traces]
    
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
                    console.print(f"[yellow]Warning: Failed to evaluate trace {result['trace_id']}: {result.get('error', 'Unknown error')}")
                
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

def save_judge_prompt(prompt: str, output_path: str) -> None:
    """Save the judge prompt to a text file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prompt)
    console.print(f"[green]Saved judge prompt to {output_path}")

def main():
    """Main function to develop the LLM judge."""
    console.print("[bold blue]LLM Judge Development")
    console.print("=" * 50)
    
    # Set up paths
    script_dir = Path(__file__).parent
    hw3_dir = script_dir.parent
    data_dir = hw3_dir / "data"
    results_dir = hw3_dir / "results"
    results_dir.mkdir(exist_ok=True)
    
    # Load data splits
    train_path = data_dir / "train_set.csv"
    dev_path = data_dir / "dev_set.csv"
    
    if not train_path.exists() or not dev_path.exists():
        console.print("[red]Error: Train or dev set not found!")
        console.print("[yellow]Please run split_data.py first.")
        return
    
    # Select few-shot examples randomly from train set
    if not OWN_PROMPT:
        train_traces = load_data_split(str(train_path))
        console.print(f"[green]Loaded {len(train_traces)} train traces")
        few_shot_examples = select_few_shot_examples(train_traces, seed=SEED)

        if not few_shot_examples:
            console.print("[red]Failed to select few-shot examples!")
            return

    # Load dev set
    dev_traces = load_data_split(str(dev_path))
    console.print(f"[green]Loaded {len(dev_traces)} dev traces")
    
    # Create judge prompt
    prompt_path = results_dir / "judge_prompt.txt"

    if OWN_PROMPT:
        console.print("[yellow]Using custom judge prompt...")
        judge_prompt = read_judge_prompt(prompt_path)
    else:
        console.print("[yellow]Using base judge prompt...")
        judge_prompt = create_judge_prompt(few_shot_examples)
    
    # Evaluate judge on dev set
    console.print("[yellow]Evaluating judge on dev set...")
    tpr, tnr, predictions = evaluate_judge_on_dev(judge_prompt, dev_traces)
    
    # Print results
    console.print(f"\n[bold]Judge Performance on Dev Set:")
    console.print(f"True Positive Rate (TPR): {tpr:.3f}")
    console.print(f"True Negative Rate (TNR): {tnr:.3f}")
    console.print(f"Balanced Accuracy: {(tpr + tnr) / 2:.3f}")
 
    # Save judge prompt
    if not OWN_PROMPT:
        save_judge_prompt(judge_prompt, str(prompt_path))
 
    # Save dev set predictions for analysis
    predictions_path = results_dir / "dev_predictions.json"
    with open(predictions_path, 'w', encoding='utf-8') as f:
        json.dump(predictions, f, indent=2)
    console.print(f"[green]Saved dev predictions to {predictions_path}")
 
    console.print("\n[bold green]Judge development completed!")
    console.print(f"[blue]Judge prompt saved to: {prompt_path}")

if __name__ == "__main__":
    main() 