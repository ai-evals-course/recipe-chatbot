# Recipe Chatbot - AI Evaluations Course

This repository contains a complete AI evaluations course built around a Recipe Chatbot. Through 5 progressive homework assignments, you'll learn practical techniques for evaluating and improving AI systems.

## Quick Start

1. **Clone & Setup**
   ```bash
   git clone https://github.com/ai-evals-course/recipe-chatbot.git
   cd recipe-chatbot
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp env.example .env
   # Edit .env to add your model and API keys
   ```

3. **Run the Chatbot**
   ```bash
   uvicorn backend.main:app --reload
   # Open http://127.0.0.1:8000
   ```

## Course Overview

### Homework Progression

1. **HW1: Basic Prompt Engineering** (`homeworks/hw1/`)
   - Write system prompts and expand test queries
   - Walkthrough: See HW2 walkthrough for HW1 content

2. **HW2: Error Analysis & Failure Taxonomy** (`homeworks/hw2/`)
   - Systematic error analysis and failure mode identification
   - **Interactive Walkthrough**:
      - Code: `homeworks/hw2/hw2_solution_walkthrough.ipynb`
      - [video 1](https://youtu.be/h9oAAAYnGx4?si=fWxN3NtpSbdD55cW): walkthrough of code
      - [video 2](https://youtu.be/AKg27L4E0M8) : open & axial coding walkthrough

3. **HW3: LLM-as-Judge Evaluation** (`homeworks/hw3/`)
   - Automated evaluation using the `judgy` library
   - **Interactive Walkthrough**:
      - Code: `homeworks/hw3/hw3_walkthrough.ipynb`
      - [video](https://youtu.be/1d5aNfslwHg): walkthrough of solution

4. **HW4: RAG/Retrieval Evaluation** (`homeworks/hw4/`)
   - BM25 retrieval system with synthetic query generation
   - **Interactive Walkthroughs**: 
     - `homeworks/hw4/hw4_walkthrough.py` (Marimo)
     - [video](https://youtu.be/GMShL5iC8aY): walkthrough of solution

5. **HW5: Agent Failure Analysis** (`homeworks/hw5/`)
   - Analyze conversation traces and failure patterns
   - **Interactive Walkthroughs**:
      - `homeworks/hw5/hw5_walkthrough.py` (Marimo)
      - [video](https://youtu.be/z1oISsDUKLA) 

### Key Features

- **Backend**: FastAPI with LiteLLM (multi-provider LLM support)
- **Frontend**: Simple chat interface with conversation history
- **Annotation Tool**: FastHTML-based interface for manual evaluation (`annotation/`)
- **Retrieval**: BM25-based recipe search (`backend/retrieval.py`)
- **Query Rewriting**: LLM-powered query optimization (`backend/query_rewrite_agent.py`)
- **Evaluation Tools**: Automated metrics, bias correction, and analysis scripts

## Project Structure

```
recipe-chatbot/
├── backend/               # FastAPI app & core logic
├── frontend/              # Chat UI (HTML/CSS/JS)
├── homeworks/             # 5 progressive assignments
│   ├── hw1/              # Prompt engineering
│   ├── hw2/              # Error analysis (with walkthrough)
│   ├── hw3/              # LLM-as-Judge (with walkthrough)
│   ├── hw4/              # Retrieval eval (with walkthroughs)
│   └── hw5/              # Agent analysis
├── annotation/            # Manual annotation tools
├── scripts/               # Utility scripts
├── data/                  # Datasets and queries
└── results/               # Evaluation outputs
```

## Running Homework Scripts

Each homework includes complete pipelines. For example:

**HW3 Pipeline:**
```bash
cd homeworks/hw3
python scripts/generate_traces.py
python scripts/label_data.py
python scripts/develop_judge.py
python scripts/evaluate_judge.py
```

**HW4 Pipeline:**
```bash
cd homeworks/hw4
python scripts/process_recipes.py
python scripts/generate_queries.py
python scripts/evaluate_retrieval.py
# Optional: python scripts/evaluate_retrieval_with_agent.py
```

## Additional Resources

- **Annotation Interface**: Run `python annotation/annotation.py` for manual evaluation
- **Bulk Testing**: Use `python scripts/bulk_test.py` to test multiple queries
- **Trace Analysis**: All conversations saved as JSON for analysis

## Multi-Turn Bulk Evaluation

Run bulk evaluations with multi-turn conversations and visualize results.

### CSV Format

Create a CSV with the following columns:
```csv
id,query,human_followup_1,human_followup_2,...
1,"How do I make pasta?","Can you suggest a vegetarian sauce?","How long should I cook it?"
2,"Show me breakfast recipes","I prefer something sweet",""
```

- `id`: Unique identifier for the conversation
- `query`: Initial user query
- `human_followup_N`: Sequential follow-up messages (optional)
  - Add as many as needed (human_followup_1, human_followup_2, etc.)
  - Empty values will be ignored

### Running Bulk Evaluation

```bash
# Run evaluation on your CSV
python scripts/bulk_test.py --csv path/to/your/queries.csv

# Results are saved to results/results_YYYYMMDD_HHMMSS.csv
```

### Viewing Results

```bash
# Generate and open HTML viewer
python scripts/view_conversations.py results/results_YYYYMMDD_HHMMSS.csv

# Generate without opening browser
python scripts/view_conversations.py results/results_YYYYMMDD_HHMMSS.csv --no-browser
```

### What to Expect

1. **During Bulk Test:**
   - Progress updates in terminal
   - Each conversation displayed with full dialogue
   - Results saved as CSV with conversation histories

2. **In HTML Viewer:**
   - Clean, paginated interface
   - One conversation per page
   - Full dialogue history with user/assistant messages
   - Easy navigation between conversations

## Environment Variables

Configure your `.env` file with:
- `MODEL_NAME`: LLM model (e.g., `openai/gpt-4`, `anthropic/claude-3-haiku-20240307`)
- API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.

See [LiteLLM docs](https://docs.litellm.ai/docs/providers) for supported providers.

## Course Philosophy

This course emphasizes:
- **Practical experience** over theory
- **Systematic evaluation** over "vibes"
- **Progressive complexity** - each homework builds on previous work
- **Industry-standard techniques** for real-world AI evaluation
