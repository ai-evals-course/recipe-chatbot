# Homework 4: Recipe Bot Retrieval Evaluation

## Note on Solutions

We've provided a walkthrough notebook (`hw4_walkthrough.ipynb`) that you can run to see the complete solution. Try the assignment yourself first - you'll learn more by working through it independently.

Video walkthrough: https://youtu.be/GMShL5iC8aY

**Bonus**: [Using AI Assisted Coding to Tackle Homework Problems](https://link.courses.maven.com/c/eJw80M2upCAQBeCngZ0Gil8XLGbja5gCymkTbAyoyX37id2Tu6rUl7OoOqm-ajuXLQeQk554qlfr9OxST8rxHHQWMhpOQTrrrFIgNacdt7Kkgr2H2CrmhP38r-fPQYHerZZCmdP7Xr5-XVsOR6t5hKSzIXKDB2MHnQwNHiQMWhIJQ-C9Q_4K3mmbY1zRC_LZw-Scw9XHKCe_Kot8CyDACimMdFIpNRpjwGaX_JogSeuZFt9_-rjjTe8x1Z1vfVlb3ZePhBlLJ17C6zyPztQfBjOD-TfNYD6wFXwnGgrGzmCmG8szQYAZFIO5_5SC8Xpsr_kq9El5J4ziLWwdMY1rwfPFtPj7VPE54w7wLwAA__8a93gB) - How to use AI coding agents (find in Maven course under Bonus)

## What You'll Do

Build and evaluate a RAG (Retrieval-Augmented Generation) component for Recipe Bot. You'll measure how well BM25 retrieval finds the right recipes for complex cooking queries.

**Example queries**:
- "What air fryer settings for frozen chicken tenders?"
- "How long to marinate beef for Korean bulgogi?"
- "What's the exact temperature for crispy roasted vegetables?"

## Dataset

This assignment uses recipe data from [Majumder et al. (2019)](https://aclanthology.org/D19-1613/) - "Generating Personalized Recipes from Historical User Preferences" (EMNLP-IJCNLP 2019).

**Full dataset**: Download from [Kaggle](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions) (180K+ recipes).

## Three Starting Points

Pick one based on how much you want to build:

### Option 1: Full Implementation

Generate everything yourself:
- Download and process the Kaggle dataset
- Generate synthetic evaluation queries
- Build and evaluate the retriever

### Option 2: Start with Processed Recipes

Use `reference_files/processed_recipes.json` (200 recipes):
- Skip data processing
- Generate your own queries
- Build and evaluate the retriever

### Option 3: Start with Queries

Use our `reference_files/synthetic_queries.jsonl` (200 queries):
- Skip data processing and query generation
- Focus on retrieval implementation and evaluation

TIP: Use `reference_files/query_viewer.html` to browse the queries. Open the HTML file in a browser and upload the JSONL file.

## Steps

### Step 1: Prepare Recipe Data (Options 1 & 2 start here)

Load and clean the recipe dataset:
- Parse ingredients, steps, tags, and nutrition
- Structure for retrieval (combine text fields for indexing)
- Save as JSON

**Option 2**: Use our `reference_files/processed_recipes.json`.

### Step 2: Generate Evaluation Queries (Option 3 starts here)

Create queries that test retrieval on specific cooking knowledge:
- Use an LLM to extract salient facts from recipes (temperatures, times, techniques)
- Generate realistic user queries that require those facts
- Save with the source recipe ID for evaluation

**Option 3**: Use our `reference_files/synthetic_queries.jsonl`.

### Step 3: Build BM25 Retriever

Implement keyword-based retrieval:
- Use `rank-bm25` library
- Index recipe text (combine name, ingredients, steps)
- Return top-k results with scores

### Step 4: Evaluate Retrieval

For each query:
1. Run the retriever
2. Check if the source recipe appears in results
3. Calculate metrics

**Metrics**:
- **Recall@1**: Target recipe at rank 1
- **Recall@3**: Target recipe in top 3
- **Recall@5**: Target recipe in top 5
- **MRR**: Mean Reciprocal Rank

### Step 5: Analyze Results

Report:
- Overall metrics
- Which query types work well vs. poorly
- Ideas for improving retrieval

## Query Types to Test

Focus on queries requiring specific recipe knowledge:
- **Appliance settings**: "Air fryer temperature for crispy vegetables?"
- **Timing specifics**: "How long to marinate chicken for teriyaki?"
- **Temperature precision**: "What internal temp for medium-rare steak?"
- **Technique details**: "How to get crispy skin on roasted chicken?"

## Expected Results

Typical BM25 performance on well-formed queries:
- Recall@5: 60-80%
- MRR: 0.4-0.7

Performance varies by query complexity and specificity.

## Deliverables

1. Working retrieval implementation
2. Evaluation results with Recall@k and MRR metrics
3. Brief analysis (1-2 paragraphs):
   - What types of queries work well vs. poorly
   - Ideas for improving retrieval performance

## Optional: Query Rewrite Agent

Improve retrieval with LLM-powered query optimization:
- **Keywords extraction**: Extract key cooking terms
- **Query rewriting**: Optimize for search effectiveness
- **Query expansion**: Add synonyms and related terms

Compare baseline BM25 with agent-enhanced retrieval and report improvements.

## Setup

1. Install: `uv pip install rank-bm25 tqdm litellm python-dotenv` (from project root)
2. Configure LLM API keys in `.env`
3. Choose your starting point and begin building.

## File Structure

```
homeworks/hw4/
├── reference_files/
│   ├── processed_recipes.json    # 200 recipes (optional starting point)
│   ├── synthetic_queries.jsonl   # 200 queries with source recipes
│   └── query_viewer.html         # Browser-based query viewer
├── hw4_walkthrough.ipynb         # Solution walkthrough (run to see expected outputs)
├── results/                      # Your evaluation outputs
└── README.md
```
