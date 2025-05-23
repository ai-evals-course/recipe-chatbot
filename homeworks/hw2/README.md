# Homework 2: Recipe Bot Error Analysis

## 📝 Note

**We have provided our solutions in this repository as reference material, but we strongly encourage you to work through the exercise on your own first.** Attempting the assignment independently will help you better understand the error analysis process and develop your own insights about chatbot failure modes.

This assignment focuses on performing an error analysis for your Recipe Bot.

## Part 1: Define Dimensions & Generate Initial Queries

1.  **Identify Key Dimensions:** (i.e., key aspects or variables of user inputs you'll use to generate diverse test queries, such as `cuisine_type`, `dietary_restriction`, or `meal_type` for your recipe bot)
    *   Identify 3-4 key dimensions relevant to your Recipe Bot's functionality and potential user inputs.
    *   For each dimension, list at least 3 example values.

2.  **Generate Unique Combinations (Tuples):**
    *   Write a prompt for a Large Language Model (LLM) to generate 15-20 unique combinations (tuples) of these dimension values.

3.  **Generate Natural Language User Queries:**
    *   Write a second prompt for an LLM to take 5-7 of the generated tuples and create a natural language user query for your Recipe Bot for each selected tuple.
    *   Review these generated queries to ensure they are realistic and representative of how a user might interact with your bot.

    **Alternative for Query Generation:** If you prefer to skip the LLM-based query generation (steps 2 and 3 above), you may use the pre-existing queries and bot responses found in `homeworks/hw2/results_20250518_215844.csv` as the basis for your error analysis in Part 2. You can then proceed directly to the "Open Coding" step using this data.

## Part 2: Initial Error Analysis (Ref Sec 3.2, 3.3, 3.4 of relevant course material)

1.  **Run Bot on Synthetic Queries:**
    *   Execute your Recipe Bot using the synthetic queries generated in Part 1.
    *   Record the full interaction traces for each query.

2.  **Open Coding:** (an initial analysis step where you review interaction traces, assigning descriptive labels/notes to identify patterns and potential errors without preconceived categories, as detailed in Sec 3.2 of the provided chapter)
    *   Review the recorded traces.
    *   Perform open coding to identify initial themes, patterns, and potential errors or areas for improvement in the bot's responses.

3.  **Axial Coding & Taxonomy Definition:** (a follow-up step where you group the initial open codes into broader, structured categories or 'failure modes' to build an error taxonomy, as described in Sec 3.3 of the provided chapter)
    *   Group the observations from open coding into broader categories or failure modes.
    *   For each identified failure mode, create a clear and concise taxonomy. This should include:
        *   **A clear Title** for the failure mode.
        *   **A concise one-sentence Definition** explaining the failure mode.
        *   **1-2 Illustrative Examples** taken directly from your bot's behavior during the tests. If a failure mode is plausible but not directly observed, you can provide a well-reasoned hypothetical example.

4.  **[Optional] Spreadsheet for Analysis:**
    *   Create a spreadsheet to systematically track your error analysis.
    *   Include the following columns:
        *   `Trace_ID` (a unique identifier for each interaction)
        *   `User_Query` (the query given to the bot)
        *   `Full_Bot_Trace_Summary` (a summary of the bot's full response and behavior)
        *   `Open_Code_Notes` (your notes and observations from the open coding process)
        *   A column for each of your 3-5 defined `Failure_Mode_Title`s (use 0 or 1 to indicate the presence or absence of that failure mode in the trace).

---

**Note:** You have the flexibility to edit, create, or modify any files within the assignment structure as needed to fulfill the requirements of this homework. This includes, but is not limited to, the `failure_mode_taxonomy.md` file, scripts for running your bot, or any spreadsheets you create for analysis. 