"""
for HW 2: Generates synthetic queries using an LLM (gpt-4o-mini via LiteLLM)
based on defined dimensions.

This script automates parts of HW2:
1. Generates unique combinations (tuples) of dimension values.
2. Generates natural language user queries from these tuples.
3. Appends the generated queries to 'synthetic_queries_for_analysis.csv'.

Prerequisites:
- Set your `OPENAI_API_KEY` environment variable for `gpt-4o-mini` access.
  (Refer to LiteLLM documentation for other providers if not using OpenAI).
"""
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import pandas as pd
from litellm import completion
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tqdm import tqdm

load_dotenv()

# --- Pydantic Models for Structured Output ---
class DimensionTuple(BaseModel):
    DietaryNeedsOrRestrictions: str
    AvailableIngredientsFocus: str
    CuisinePreference: str
    SkillLevelEffort: str
    TimeAvailability: str
    QueryStyleAndDetail: str

class QueryWithDimensions(BaseModel):
    id: str
    query: str
    dimension_tuple: DimensionTuple
    is_realistic_and_kept: int = 1
    notes_for_filtering: str = ""

class DimensionTuplesList(BaseModel):
    tuples: List[DimensionTuple]

class QueriesList(BaseModel):
    queries: List[str]

# --- Configuration ---
MODEL_NAME = "gpt-4o-mini"
NUM_TUPLES_TO_GENERATE = 10  # Generate more tuples than needed to ensure diversity
NUM_QUERIES_PER_TUPLE = 5    # Generate multiple queries per tuple
OUTPUT_CSV_PATH = Path(__file__).parent / "synthetic_queries_for_analysis.csv"
MAX_WORKERS = 5  # Number of parallel LLM calls

def call_llm(messages: List[Dict[str, str]], response_format: Any) -> Any:
    """Make a single LLM call with retries."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = completion(
                model=MODEL_NAME,
                messages=messages,
                response_format=response_format
            )
            return response_format(**json.loads(response.choices[0].message.content))
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)  # Wait before retry

def generate_dimension_tuples() -> List[DimensionTuple]:
    """Generate diverse dimension tuples."""
    prompt = f"""Generate {NUM_TUPLES_TO_GENERATE} diverse combinations of dimension values for a recipe chatbot.
Each combination should represent a different user scenario. Ensure balanced coverage across all dimensions - don't over-represent any particular value or combination.

Important: Aim for an even distribution across all dimensions. For example:
- Don't generate too many dietary restrictions combinations
- Don't focus too heavily on quick recipes
- Don't over-represent any particular cuisine
- Vary the query styles naturally
- Try to use weird combinations of ingredients required in AvailableIngredientsFocus

DietaryNeedsOrRestrictions:
- vegan, vegetarian, gluten-free, dairy-free, keto, paleo, halal, kosher, no restrictions, pescatarian, low-carb, low-sodium, nut-free, egg-free, soy-free, FODMAP, diabetic-friendly, high-protein

AvailableIngredientsFocus:
- must_use_specific: [list of ingredients]
- general_pantry: basic ingredients
- no_specific_ingredients: open to suggestions

CuisinePreference:
- specific_cuisine: [cuisine type]
- any_cuisine
- avoid_specific: [cuisine type]

SkillLevelEffort:
- beginner_easy_low_effort
- intermediate_moderate_effort
- advanced_complex_high_effort

TimeAvailability:
- quick_under_30_mins
- moderate_30_to_60_mins
- flexible_no_time_constraint

QueryStyleAndDetail:
- short_keywords_minimal_detail
- natural_question_moderate_detail
- detailed_request_high_detail

Here are some example dimension tuples that show realistic combinations:

1. Beginner cook with time constraints and specific ingredients:
{{
    "DietaryNeedsOrRestrictions": "no restrictions",
    "AvailableIngredientsFocus": "must_use_specific: chicken breast, rice, vegetables",
    "CuisinePreference": "any_cuisine",
    "SkillLevelEffort": "beginner_easy_low_effort",
    "TimeAvailability": "quick_under_30_mins",
    "QueryStyleAndDetail": "natural_question_moderate_detail"
}}

2. Experienced cook with dietary restrictions and flexible time:
{{
    "DietaryNeedsOrRestrictions": "vegan",
    "AvailableIngredientsFocus": "general_pantry",
    "CuisinePreference": "specific_cuisine: mediterranean",
    "SkillLevelEffort": "advanced_complex_high_effort",
    "TimeAvailability": "flexible_no_time_constraint",
    "QueryStyleAndDetail": "detailed_request_high_detail"
}}

3. Busy parent with dietary needs and pantry ingredients:
{{
    "DietaryNeedsOrRestrictions": "gluten_free",
    "AvailableIngredientsFocus": "general_pantry",
    "CuisinePreference": "avoid_specific: spicy",
    "SkillLevelEffort": "intermediate_moderate_effort",
    "TimeAvailability": "moderate_30_to_60_mins",
    "QueryStyleAndDetail": "short_keywords_minimal_detail"
}}

4. Student with limited ingredients and quick time:
{{
    "DietaryNeedsOrRestrictions": "vegetarian",
    "AvailableIngredientsFocus": "must_use_specific: pasta, canned tomatoes, cheese",
    "CuisinePreference": "any_cuisine",
    "SkillLevelEffort": "beginner_easy_low_effort",
    "TimeAvailability": "quick_under_30_mins",
    "QueryStyleAndDetail": "natural_question_moderate_detail"
}}

5. Food enthusiast with specific cuisine preference:
{{
    "DietaryNeedsOrRestrictions": "no restrictions",
    "AvailableIngredientsFocus": "no_specific_ingredients",
    "CuisinePreference": "specific_cuisine: thai",
    "SkillLevelEffort": "intermediate_moderate_effort",
    "TimeAvailability": "moderate_30_to_60_mins",
    "QueryStyleAndDetail": "detailed_request_high_detail"
}}

Generate {NUM_TUPLES_TO_GENERATE} unique dimension tuples following these patterns. Remember to maintain balanced diversity across all dimensions."""

    messages = [{"role": "user", "content": prompt}]
    
    try:
        print("Generating dimension tuples in parallel...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit five generation tasks using a loop
            futures = []
            for _ in range(5):
                futures.append(executor.submit(call_llm, messages, DimensionTuplesList))
            
            # Wait for all to complete and collect results
            responses = []
            for future in futures:
                responses.append(future.result())
        
        # Combine tuples and remove duplicates
        all_tuples = []
        for response in responses:
            all_tuples.extend(response.tuples)
        unique_tuples = []
        seen = set()
        
        for tup in all_tuples:
            # Convert tuple to a comparable string representation
            tuple_str = tup.model_dump_json()
            if tuple_str not in seen:
                seen.add(tuple_str)
                unique_tuples.append(tup)
        
        print(f"Generated {len(all_tuples)} total tuples, {len(unique_tuples)} unique")
        return unique_tuples
    except Exception as e:
        print(f"Error generating dimension tuples: {e}")
        return []

def generate_queries_for_tuple(dimension_tuple: DimensionTuple) -> List[str]:
    """Generate natural language queries for a given dimension tuple."""
    prompt = f"""Generate {NUM_QUERIES_PER_TUPLE} different natural language queries for a recipe chatbot based on these characteristics:
{dimension_tuple.model_dump_json(indent=2)}

The queries should:
1. Sound like real users asking for recipe help
2. Naturally incorporate all the dimension values
3. Vary in style and detail level
4. Be realistic and practical
5. Include natural variations in typing style, such as:
   - Some queries in all lowercase
   - Some with random capitalization
   - Some with common typos
   - Some with missing punctuation
   - Some with extra spaces or missing spaces
   - Some with emojis or text speak

Here are examples of realistic query variations for a beginner, vegan, quick recipe:

Proper formatting:
- "Need a simple vegan dinner that's ready in 20 minutes"
- "What's an easy plant-based recipe I can make quickly?"

All lowercase:
- "need a quick vegan recipe for dinner"
- "looking for easy plant based meals"

Random caps:
- "NEED a Quick Vegan DINNER recipe"
- "what's an EASY plant based recipe i can make"

Common typos:
- "need a quik vegan recip for dinner"
- "wat's an easy plant based recipe i can make"

Missing punctuation:
- "need vegan dinner ideas quick"
- "easy plant based recipe 20 mins"

With emojis/text speak:
- "need vegan dinner ideas asap! 🥗"
- "pls help with quick plant based recipe thx"

Generate {NUM_QUERIES_PER_TUPLE} unique queries that match the given dimensions, varying the text style naturally."""

    messages = [{"role": "user", "content": prompt}]
    
    try:
        response = call_llm(messages, QueriesList)
        return response.queries
    except Exception as e:
        print(f"Error generating queries for tuple: {e}")
        return []

def generate_queries_parallel(dimension_tuples: List[DimensionTuple]) -> List[QueryWithDimensions]:
    """Generate queries in parallel for all dimension tuples."""
    all_queries = []
    query_id = 1
    
    print(f"Generating {NUM_QUERIES_PER_TUPLE} queries each for {len(dimension_tuples)} dimension tuples...")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all query generation tasks
        future_to_tuple = {
            executor.submit(generate_queries_for_tuple, dim_tuple): i 
            for i, dim_tuple in enumerate(dimension_tuples)
        }
        
        # Process completed generations as they finish
        with tqdm(total=len(dimension_tuples), desc="Generating Queries") as pbar:
            for future in as_completed(future_to_tuple):
                tuple_idx = future_to_tuple[future]
                try:
                    queries = future.result()
                    if queries:
                        for query in queries:
                            all_queries.append(QueryWithDimensions(
                                id=f"SYN{query_id:03d}",
                                query=query,
                                dimension_tuple=dimension_tuples[tuple_idx]
                            ))
                            query_id += 1
                    pbar.update(1)
                except Exception as e:
                    print(f"Tuple {tuple_idx + 1} generated an exception: {e}")
                    pbar.update(1)
    
    return all_queries

def save_queries_to_csv(queries: List[QueryWithDimensions]):
    """Save generated queries to CSV using pandas."""
    if not queries:
        print("No queries to save.")
        return

    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'id': q.id,
            'query': q.query,
            'dimension_tuple_json': q.dimension_tuple.model_dump_json(),
            'is_realistic_and_kept': q.is_realistic_and_kept,
            'notes_for_filtering': q.notes_for_filtering
        }
        for q in queries
    ])
    
    # Save to CSV
    df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Saved {len(queries)} queries to {OUTPUT_CSV_PATH}")

def main():
    """Main function to generate and save queries."""
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    start_time = time.time()
    
    # Step 1: Generate dimension tuples
    print("Step 1: Generating dimension tuples...")
    dimension_tuples = generate_dimension_tuples()
    if not dimension_tuples:
        print("Failed to generate dimension tuples. Exiting.")
        return
    print(f"Generated {len(dimension_tuples)} dimension tuples.")
    
    # Step 2: Generate queries for each tuple
    print("\nStep 2: Generating natural language queries...")
    queries = generate_queries_parallel(dimension_tuples)
    
    if queries:
        save_queries_to_csv(queries)
        elapsed_time = time.time() - start_time
        print(f"\nQuery generation completed successfully in {elapsed_time:.2f} seconds.")
        print(f"Generated {len(queries)} queries from {len(dimension_tuples)} dimension tuples.")
    else:
        print("Failed to generate any queries.")

if __name__ == "__main__":
    main() 