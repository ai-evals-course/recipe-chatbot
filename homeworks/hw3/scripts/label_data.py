#!/usr/bin/env python3
"""Label Recipe Bot traces for dietary adherence using GPT-4o.

This script can be used as a powerful automatic labeler to create ground
truth labels for whether Recipe Bot responses properly adhere to dietary restrictions.
It uses GPT-4o as a powerful labeler and also comes with a well designed and tested 
labeling prompt.

Remember that automatic creation of ground truth labels should never be used without
also looking extensively at the data. This script is intended as a fast way to give
you "ground truth" for this homework assignment.
"""

import pandas as pd
import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.progress import track
import litellm
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()

MAX_WORKERS = 32

console = Console()

# Labeling prompt for GPT-4o
LABELING_PROMPT = """You are an expert nutritionist and dietary specialist. Your task is to evaluate whether a recipe response properly adheres to the specified dietary restriction.

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
- PASS: The recipe clearly adheres to the dietary restriction with appropriate ingredients and preparation methods
- FAIL: The recipe contains ingredients or methods that violate the dietary restriction
- Consider both explicit ingredients and cooking methods
- Be strict but reasonable in your evaluation

Please analyze the query, dietary restriction, and recipe response, then provide your evaluation.

Query: {query}
Dietary Restriction: {dietary_restriction}
Recipe Response: {response}

Provide your analysis in the following JSON format:
{{
    "reasoning": "Detailed explanation of your evaluation, citing specific ingredients or methods",
    "label": "PASS" or "FAIL",
    "confidence": "HIGH", "MEDIUM", or "LOW"
}}"""

def load_traces(csv_path: str) -> List[Dict[str, Any]]:
    """Load traces from CSV file."""
    df = pd.read_csv(csv_path)
    return df.to_dict('records')

def get_labeling_response(query: str, dietary_restriction: str, response: str) -> Optional[Dict[str, Any]]:
    """Get labeling response from GPT-4o."""
    try:
        prompt = LABELING_PROMPT.format(
            query=query,
            dietary_restriction=dietary_restriction,
            response=response
        )
        
        completion = litellm.completion(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        # Try to parse JSON response
        try:
            # Extract JSON from response if it's wrapped in markdown
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
            return result
        except json.JSONDecodeError:
            console.print(f"[yellow]Warning: Could not parse JSON response: {response_text}")
            return None
            
    except Exception as e:
        console.print(f"[red]Error getting labeling response: {str(e)}")
        return None

def label_single_trace(trace: Dict[str, Any]) -> Dict[str, Any]:
    """Label a single trace using GPT-4o."""
    query = trace["query"]
    dietary_restriction = trace["dietary_restriction"]
    response = trace["response"]
    
    labeling_result = get_labeling_response(query, dietary_restriction, response)
    
    if labeling_result:
        labeled_trace = trace.copy()
        labeled_trace.update({
            "label": labeling_result.get("label"),
            "reasoning": labeling_result.get("reasoning"),
            "confidence": labeling_result.get("confidence"),
            "labeled": True
        })
    else:
        labeled_trace = trace.copy()
        labeled_trace.update({
            "label": None,
            "reasoning": None,
            "confidence": None,
            "labeled": False
        })
    
    return labeled_trace

def label_traces(traces: List[Dict[str, Any]], 
                sample_size: int = 150, 
                max_workers: int = MAX_WORKERS) -> List[Dict[str, Any]]:
    """Label a sample of traces using GPT-4o with parallel processing."""
    # Sample traces for labeling
    if len(traces) > sample_size:
        sampled_traces = random.sample(traces, sample_size)
    else:
        sampled_traces = traces
    
    labeled_traces = []
    
    # Use ThreadPoolExecutor for parallel labeling
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all labeling tasks
        future_to_trace = {executor.submit(label_single_trace, trace): trace for trace in sampled_traces}
        
        # Process completed tasks with progress tracking
        with console.status("[yellow]Labeling traces with GPT-4o in parallel...") as status:
            completed = 0
            total = len(sampled_traces)
            
            for future in as_completed(future_to_trace):
                labeled_trace = future.result()
                labeled_traces.append(labeled_trace)
                completed += 1
                
                status.update(f"[yellow]Labeled {completed}/{total} traces ({completed/total*100:.1f}%)")
    
    console.print(f"[green]Completed parallel labeling of {len(labeled_traces)} traces")
    return labeled_traces

def balance_labels(labeled_traces: List[Dict[str, Any]], 
                  target_positive: int = 75, 
                  target_negative: int = 75) -> List[Dict[str, Any]]:
    """Balance the dataset to have roughly equal positive and negative examples."""
    # Filter successfully labeled traces
    valid_traces = [t for t in labeled_traces if t["labeled"] and t["label"] in ["PASS", "FAIL"]]
    
    pass_traces = [t for t in valid_traces if t["label"] == "PASS"]
    fail_traces = [t for t in valid_traces if t["label"] == "FAIL"]
    
    console.print(f"[blue]Available traces: {len(pass_traces)} PASS, {len(fail_traces)} FAIL")
    
    # Sample to get balanced dataset
    selected_pass = random.sample(pass_traces, min(target_positive, len(pass_traces)))
    selected_fail = random.sample(fail_traces, min(target_negative, len(fail_traces)))
    
    balanced_traces = selected_pass + selected_fail
    random.shuffle(balanced_traces)
    
    console.print(f"[green]Balanced dataset: {len(selected_pass)} PASS, {len(selected_fail)} FAIL")
    
    return balanced_traces

def save_labeled_traces(traces: List[Dict[str, Any]], output_path: str) -> None:
    """Save labeled traces to CSV file."""
    df = pd.DataFrame(traces)
    df.to_csv(output_path, index=False)
    console.print(f"[green]Saved {len(traces)} labeled traces to {output_path}")

def main():
    """Main function to label traces."""
    console.print("[bold blue]Recipe Bot Trace Labeling")
    console.print("=" * 50)
    
    # Set up paths
    script_dir = Path(__file__).parent
    hw3_dir = script_dir.parent
    data_dir = hw3_dir / "data"
    
    # Load raw traces
    traces_path = data_dir / "raw_traces.csv"
    if not traces_path.exists():
        console.print(f"[red]Error: {traces_path} not found!")
        console.print("[yellow]Please run generate_traces.py first.")
        return
    
    traces = load_traces(str(traces_path))
    console.print(f"[green]Loaded {len(traces)} traces")
    
    # Label traces with parallel processing
    console.print("[yellow]Labeling traces with GPT-4o using parallel processing...")
    labeled_traces = label_traces(traces, sample_size=200, max_workers=MAX_WORKERS)  # Label more than needed
    
    # Balance the dataset
    balanced_traces = balance_labels(labeled_traces, target_positive=75, target_negative=75)
    
    # Save labeled traces
    output_path = data_dir / "labeled_traces.csv"
    save_labeled_traces(balanced_traces, str(output_path))
    
    # Print summary statistics
    console.print("\n[bold]Labeling Summary:")
    console.print(f"Total labeled traces: {len(balanced_traces)}")
    
    label_counts = {}
    confidence_counts = {}
    for trace in balanced_traces:
        label = trace["label"]
        confidence = trace["confidence"]
        label_counts[label] = label_counts.get(label, 0) + 1
        confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
    
    console.print("\nLabel distribution:")
    for label, count in sorted(label_counts.items()):
        console.print(f"  {label}: {count}")
    
    console.print("\nConfidence distribution:")
    for confidence, count in sorted(confidence_counts.items()):
        console.print(f"  {confidence}: {count}")

if __name__ == "__main__":
    main() 