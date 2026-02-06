# Homework 2: Recipe Bot Error Analysis

## Note on Solutions

We've provided a walkthrough notebook (`hw2_walkthrough.ipynb`) that you can run to see the complete solution. Try the assignment yourself first - you'll learn more by working through it independently.

Video walkthrough: https://youtu.be/h9oAAAYnGx4

**Bonus**: [Using AI Assisted Coding to Tackle Homework Problems](https://link.courses.maven.com/c/eJw80M2upCAQBeCngZ0Gil8XLGbja5gCymkTbAyoyX37id2Tu6rUl7OoOqm-ajuXLQeQk554qlfr9OxST8rxHHQWMhpOQTrrrFIgNacdt7Kkgr2H2CrmhP38r-fPQYHerZZCmdP7Xr5-XVsOR6t5hKSzIXKDB2MHnQwNHiQMWhIJQ-C9Q_4K3mmbY1zRC_LZw-Scw9XHKCe_Kot8CyDACimMdFIpNRpjwGaX_JogSeuZFt9_-rjjTe8x1Z1vfVlb3ZePhBlLJ17C6zyPztQfBjOD-TfNYD6wFXwnGgrGzmCmG8szQYAZFIO5_5SC8Xpsr_kq9El5J4ziLWwdMY1rwfPFtPj7VPE54w7wLwAA__8a93gB) - How to use AI coding agents (find in Maven course under Bonus)

## What You'll Do

Find and categorize the ways your Recipe Bot fails. You'll generate test queries, run your bot, and build a taxonomy of failure modes.

## Part 1: Generate Test Queries

### Step 1: Pick Your Dimensions

Choose 3-4 dimensions that matter for recipe queries. Examples:
- Cuisine type (Italian, Thai, Mexican)
- Dietary restrictions (vegan, gluten-free, keto)
- Meal type (breakfast, dinner, snack)

List at least 3 values for each dimension.

### Step 2: Create Combinations

Write an LLM prompt to generate 15-20 unique combinations of your dimension values.
Review combinations and remove any that are not realistic for a user to ask.

### Step 3: Turn Combinations into Queries

Write another LLM prompt to convert 5-7 combinations into natural language queries that users might actually ask.

Review the queries. Do they sound realistic?

**Skip Steps 2-3?** Use the pre-existing queries in `homeworks/hw2/reference_files/query_response.jsonl` and jump to Part 2, step 1.  You can use the viewer in that directory to first **look at your data**.

## Part 2: Find and Categorize Errors

> Ref Sec 3.2, 3.3, 3.4 of relevant course material

### Step 1: Run Your Bot

Execute your Recipe Bot on your queries. Save the full conversation traces.

### Step 2: Open Coding

Read through the traces. Note patterns, errors, and anything unusual. Don't use categories yet—just observe and take notes.

See Section 3.2 of the course material for details.

Watch [Isaac & Hamel do open & axial coding](https://youtu.be/AKg27L4E0M8) : open & axial coding walkthrough

### Step 3: Build Your Taxonomy

Group your observations into failure modes. For each one, write:
- **Title**: Clear name for the failure
- **Definition**: One sentence explaining it
- **Examples**: 1-2 real examples from your tests (or well-reasoned hypothetical examples if you didn't observe it)

**Use the template**: Edit `failure_mode_taxonomy.md` to document your failure modes. This file provides a structured format with examples to help you organize your taxonomy.

See Sections 3.3-3.4 of the course material.

### Step 4: Track It (Optional)

Create a spreadsheet with these columns:
- `Trace_ID`: Unique identifier for each test
- `User_Query`: What the user asked
- `Full_Bot_Trace_Summary`: What the bot did
- `Open_Code_Notes`: Your observations
- One column per failure mode (mark 0 or 1)

**Tool**: Use any tool you are comfortable with (csv, google sheets, excel, notebook, etc.)

## Working in This Assignment

Edit any files you need. Create new scripts. Modify `failure_mode_taxonomy.md`. The structure is flexible.

## File Structure

```
homeworks/hw2/
├── reference_files/
│   ├── query_response.jsonl       # 250 query/response pairs (optional starting point)
│   ├── failure_mode_taxonomy.md   # Template for documenting failure modes
│   └── viewer.html                # Browser-based viewer for the JSONL file
├── hw2_walkthrough.ipynb          # Solution walkthrough (run to see expected outputs)
└── README.md
```

TIP: Open `reference_files/viewer.html` in your browser and upload the JSONL file to browse the data interactively.
