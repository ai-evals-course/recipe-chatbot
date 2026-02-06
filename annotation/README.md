# Annotation Tool

A FastHTML web application for annotating recipe chatbot query/response pairs using qualitative coding methods.

## Purpose

This tool enables manual annotation of chatbot traces for qualitative analysis. It supports two types of coding:

1. **Open Coding** - Free-form text notes to capture observations, issues, or patterns in each response
2. **Axial Coding** - Categorical labels (failure modes, quality issues, etc.) that can be selected from existing codes or new ones can be added

## Running the Application

```bash
cd annotation
uv run python annotation.py
```

The app runs at http://localhost:5001

## Data Format

Traces are stored as individual JSON files in `annotation/traces/` with this structure:

```json
{
  "request": {
    "messages": [{"role": "user", "content": "user query..."}]
  },
  "response": {
    "messages": [
      {"role": "system", "content": "system prompt..."},
      {"role": "user", "content": "user query..."},
      {"role": "assistant", "content": "assistant response..."}
    ]
  },
  "id": "SYN001",
  "open_coding": "",
  "axial_coding_code": ""
}
```

## Converting JSONL to Traces

To convert query/response JSONL data to the trace format:

```python
import json
import os

input_file = "path/to/query_response.jsonl"
output_dir = "annotation/traces"

with open(input_file, 'r') as f:
    for idx, line in enumerate(f):
        data = json.loads(line.strip())
        trace = {
            "request": {"messages": [{"role": "user", "content": data["query"]}]},
            "response": {
                "messages": [
                    {"role": "system", "content": "You are a helpful recipe assistant."},
                    {"role": "user", "content": data["query"]},
                    {"role": "assistant", "content": data["response"]}
                ]
            },
            "id": data.get("id", f"SYN{idx:03d}"),
            "open_coding": "",
            "axial_coding_code": ""
        }
        filename = f"trace_2024-01-15_12{idx:04d}.json"
        with open(os.path.join(output_dir, filename), 'w') as out:
            json.dump(trace, out, indent=2)
```

## Workflow

1. Navigate to the home page to see all traces
2. Click a trace to view the conversation and add annotations
3. Add open coding notes in the text area
4. Select or create axial coding categories from the dropdown
5. Press Save (or Ctrl+Enter) to save and advance to the next trace
6. Annotated traces show ✅ checkmarks on the home page

## Key Files

- `annotation.py` - Main FastHTML application
- `traces/` - Directory containing JSON trace files (annotations saved in-place)
