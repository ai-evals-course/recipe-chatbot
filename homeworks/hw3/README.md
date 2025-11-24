# Homework 3: LLM-as-Judge for Recipe Bot Evaluation

## Your Task

Measure how well your Recipe Bot follows dietary restrictions. Build an LLM judge, correct its biases, and report confidence intervals.

**Example**: If a user asks for a vegan recipe, does the bot deliver one that's actually vegan?

## What You Get

- ~2000 Recipe Bot traces (optional starting point)
- Defined criteria for dietary adherence
- The `judgy` Python library: [github.com/ai-evals-course/judgy](https://github.com/ai-evals-course/judgy)

We picked dietary adherence because the rules are clear and objective.

**Alternative**: Choose a different failure mode from HW2. You'll need to define your own criteria and generate your own traces.

## Three Starting Points

Pick one based on how much you want to build:

### Option 1: Full Implementation

Generate everything yourself:
- Create your own Recipe Bot traces
- Label your own data
- Build the complete pipeline

### Option 2: Start with Traces

Use `reference_files/raw_traces.jsonl` (~2400 traces):
- Skip trace generation
- Label a subset yourself
- Build the judge and evaluation

Our traces use `reference_files/dietary_queries.csv`—60 challenging edge cases we wrote.

TIP:  Use `reference_files/trace_viewer.html` to look at the traces.  It was generated with claude code and the following query:

> "Make a self contained HTML file to view the jsonl files.  It should instruct to upload one of the 2 files to a 
viewer, where people can navigate between the traces and see all the info in a minimal, but reasonable way."

### Option 3: Start with Labels

Use our `reference_files/labeled_traces.jsonl` (101 labeled examples):
- Skip trace generation and labeling
- Focus on judge development
- Apply statistical corrections

TIP:  Use `reference_files/trace_viewer.html` to look at the traces.  It was generated with claude code and the following query:

> "Make a self contained HTML file to view the jsonl files.  It should instruct to upload one of the 2 files to a 
viewer, where people can navigate between the traces and see all the info in a minimal, but reasonable way."

## Steps

### Step 1: Label Your Data (Options 1 & 2 start here)

Label 100-200 traces as Pass or Fail. This is your ground truth.

- **Option 1**: Generate traces first, then label them. See `input/dietary_queries.csv` for query ideas.
- **Option 2**: Use our `reference_files/raw_traces.jsonl`, then label a subset.

> Note: The skill of labeling is undervalued and is often a massive step that is not done enough in commercial applications.  If you want to have the biggest impact, labeling traces is crucial.

### Step 2: Split Your Data (Option 3 starts here)

Divide labeled data into:
- Train: 10-20%
- Dev: 40%
- Test: 40-50%

**Option 3**: Split our `reference_files/labeled_traces.jsonl`.

### Step 3: Write Your Judge Prompt

Include:
- The task and criterion
- Clear Pass/Fail definitions
- 2-3 few-shot examples from your Train set with input, output, reasoning, and pass/fail label
- Expected output format (JSON with reasoning and Pass/Fail)

### Step 4: Test and Refine

- Test your judge on the Dev set
- Measure True Positive Rate (TPR) and True Negative Rate (TNR)
- Refine until you're satisfied
- Report final TPR and TNR on your Test set

### Step 5: Evaluate New Traces

Run your judge on 500-1000 new traces (from the provided set or generate your own).

### Step 6: Report Results

Use `judgy` to calculate and report:
- Raw pass rate (p_obs)
- Corrected success rate (θ̂)
- 95% Confidence Interval
- Brief interpretation (1-2 paragraphs).  How well is the Recipe Bot adhering to dietary preferences? How confident are you in this assessment?

## Dietary Adherence Criterion

**Definition**: The bot should provide recipes that actually meet the user's stated dietary restrictions.

**Examples**:

Pass:
- User asks for vegan pasta → Bot suggests nutritional yeast instead of parmesan
- User asks for gluten-free bread → Bot uses almond flour and xanthan gum
- User asks for keto dinner → Bot provides cauliflower rice with high-fat protein

Fail:
- User asks for vegan pasta → Bot includes honey (not vegan)
- User asks for gluten-free bread → Bot uses regular soy sauce (contains wheat)
- User asks for keto dinner → Bot includes sweet potato (too many carbs)

### Common Dietary Restrictions

(Reference from OpenAI o4)

- **Vegan**: No animal products (meat, dairy, eggs, honey, etc.)
- **Vegetarian**: No meat or fish, but dairy and eggs are allowed
- **Gluten-free**: No wheat, barley, rye, or other gluten-containing grains
- **Dairy-free**: No milk, cheese, butter, yogurt, or other dairy products
- **Keto**: Very low carb (typically <20g net carbs), high fat, moderate protein
- **Paleo**: No grains, legumes, dairy, refined sugar, or processed foods
- **Pescatarian**: No meat except fish and seafood
- **Kosher**: Follows Jewish dietary laws (no pork, shellfish, mixing meat/dairy)
- **Halal**: Follows Islamic dietary laws (no pork, alcohol, proper slaughter)
- **Nut-free**: No tree nuts or peanuts
- **Low-carb**: Significantly reduced carbohydrates (typically <50g per day)
- **Sugar-free**: No added sugars or high-sugar ingredients
- **Raw vegan**: Vegan foods not heated above 118°F (48°C)
- **Whole30**: No grains, dairy, legumes, sugar, alcohol, or processed foods
- **Diabetic-friendly**: Low glycemic index, controlled carbohydrates
- **Low-sodium**: Reduced sodium content for heart health

## Challenging Queries

**Contradictory requests**:
- "I'm vegan but I really want to make something with honey - is there a good substitute?"
- "I want a cheeseburger but I'm dairy-free and vegetarian"

**Ambiguous preferences**:
- "Something not too carb-y for dinner"
- "Something keto-ish but not super strict"
- "Dairy-free but cheese is okay sometimes"

## Key Metrics

- **True Positive Rate (TPR)**: How often the judge correctly identifies adherent recipes
- **True Negative Rate (TNR)**: How often the judge correctly identifies non-adherent recipes  
- **Corrected Success Rate**: True adherence rate accounting for judge errors
- **95% Confidence Interval**: Range for the corrected success rate

## Deliverables

1. Labeled dataset with train/dev/test splits
2. Final judge prompt with few-shot examples
3. Judge performance (TPR/TNR on test set)
4. Final evaluation using judgy (raw rate, corrected rate, CI)
5. Brief analysis (1-2 paragraphs)

### Our Results

```bash
Raw Observed Success Rate: 0.857 (85.7%)
Corrected Success Rate: 0.926 (92.6%)
95% Confidence Interval: [0.817, 1.000]
                        [81.7%, 100.0%]
Correction Applied: 0.069 (6.9 percentage points)
```

This suggests the Recipe Bot has strong dietary adherence (92.6% corrected success rate), with the judge initially underestimating performance due to false negatives. The 6.9 percentage point correction indicates our judge had some bias that was successfully accounted for using the judgy library.

## Setup

1. Install: `uv pip install -r requirements.txt` (from project root)
2. Configure LLM API keys in `.env`
3. Choose your failure mode and begin labeling!

Good luck with your evaluation!