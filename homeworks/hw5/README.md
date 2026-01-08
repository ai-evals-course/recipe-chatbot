# Homework 5: Failure Transition Heat-Map

## Note on Solutions

We've provided a walkthrough notebook (`hw5_walkthrough.ipynb`) that you can run to see the complete solution. Try the assignment yourself first - you'll learn more by working through it independently.

Video walkthrough: https://youtu.be/z1oISsDUKLA

**Bonus**: [Using AI Assisted Coding to Tackle Homework Problems](https://link.courses.maven.com/c/eJw80M2upCAQBeCngZ0Gil8XLGbja5gCymkTbAyoyX37id2Tu6rUl7OoOqm-ajuXLQeQk554qlfr9OxST8rxHHQWMhpOQTrrrFIgNacdt7Kkgr2H2CrmhP38r-fPQYHerZZCmdP7Xr5-XVsOR6t5hKSzIXKDB2MHnQwNHiQMWhIJQ-C9Q_4K3mmbY1zRC_LZw-Scw9XHKCe_Kot8CyDACimMdFIpNRpjwGaX_JogSeuZFt9_-rjjTe8x1Z1vfVlb3ZePhBlLJ17C6zyPztQfBjOD-TfNYD6wFXwnGgrGzmCmG8szQYAZFIO5_5SC8Xpsr_kq9El5J4ziLWwdMY1rwfPFtPj7VPE54w7wLwAA__8a93gB) - How to use AI coding agents (find in Maven course under Bonus)

## What You'll Do

Analyze where your cooking-assistant agent fails. Every conversation trace contains one failure. Build a transition matrix showing where the agent succeeds last and where it fails first, then visualize the result as a heat-map.

You do not need to call any LLMs or generate any additional data. All classification work has already been done for you.

## Data Provided

`reference_files/labeled_traces.jsonl` contains 96 traces, one JSON object per line:

```json
{
  "conversation_id": "a1b2...",
  "messages": [ {"role": "user", "content": "..."}, ... ],
  "last_success_state": "GetRecipes",
  "first_failure_state": "GetWebInfo"
}
```

The two state fields form a directed edge that you will count in the transition matrix.

TIP: Use `reference_files/trace_viewer.html` to browse the traces. Open the HTML file in a browser and upload the JSONL file.

## Pipeline State Taxonomy

The agent's internal pipeline is abstracted to 10 canonical states:

| # | State | Description |
|---|--------------------|-------------------------------------------|
| 1 | `ParseRequest`     | LLM interprets the user's message         |
| 2 | `PlanToolCalls`    | LLM decides which tools to invoke         |
| 3 | `GenCustomerArgs`  | LLM constructs arguments for customer DB  |
| 4 | `GetCustomerProfile` | Executes customer-profile tool         |
| 5 | `GenRecipeArgs`    | LLM constructs arguments for recipe DB    |
| 6 | `GetRecipes`       | Executes recipe-search tool               |
| 7 | `GenWebArgs`       | LLM constructs arguments for web search   |
| 8 | `GetWebInfo`       | Executes web-search tool                  |
| 9 | `ComposeResponse`  | LLM drafts the final answer               |
|10 | `DeliverResponse`  | Agent sends the answer                    |

Every trace succeeds through `last_success_state` and then fails at `first_failure_state`.

## Steps

### Step 1: Inspect the Data

Familiarize yourself with the JSONL structure and the state list above.

### Step 2: Build the Transition Matrix

Count how many times each `(last_success → first_failure)` pair appears.

### Step 3: Visualize

Render a heat-map where rows = last-success, columns = first-failure.

A starter script is provided:
```bash
cd homeworks/hw5
python analysis/transition_heatmaps.py
```

This writes `results/failure_transition_heatmap.png`.

### Step 4: Analyze

- Which states fail most often?
- Do failures cluster around tool execution or argument generation?
- Any surprising low-frequency transitions?

### Step 5: Deliverables

- Heat-map PNG (commit to `results/`)
- Short write-up (README or a separate markdown file) summarizing your findings

## File Structure

```
homeworks/hw5/
├── reference_files/
│   ├── labeled_traces.jsonl     # 96 labeled traces
│   ├── raw_traces.jsonl         # Raw conversations (for reference)
│   └── trace_viewer.html        # Browser-based trace viewer
├── analysis/
│   └── transition_heatmaps.py   # Starter script (you may modify)
├── hw5_walkthrough.ipynb        # Solution walkthrough (run to see expected outputs)
├── results/
│   └── failure_transition_heatmap.png  # Your output
└── README.md
```

## Setup

1. Install: `uv pip install numpy matplotlib seaborn` (from project root)
2. Run the analysis script to generate your heatmap.

Good luck with your analysis.
