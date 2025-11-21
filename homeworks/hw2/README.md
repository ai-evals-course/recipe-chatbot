# Homework 2: Recipe Bot Error Analysis

## Note on Solutions

We've provided solutions in this repository, but try the assignment yourself first. You'll learn more by working through it independently.

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
