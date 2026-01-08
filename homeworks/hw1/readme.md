# Homework Assignment 1: Write a Starting Prompt

## Overview

The purpose of homework 1 is to understand the basics of writing a system prompt and creating example data.

## Part1: Write an Effective System Prompt

**Assignment:** Replace `backend/system_prompt.md` with a well-crafted system prompt.

**Tasks:**
- [ ] **Define the Bot's Role & Objective**: Clearly state what the bot is. (e.g., _You are a friendly and creative culinary assistant specializing in suggesting easy-to-follow recipes._)
- [ ] **Response Rules**: Be specific.
    + What should it *always* do?  Examples:
        + _Always provide ingredient lists with precise measurements using standard units._
        + _Always include clear, step-by-step instructions._
    + What should it *never* do? Examples: 
        + _Never suggest recipes that require extremely rare or unobtainable ingredients without providing readily available alternatives._
        + _Never use offensive or derogatory language._
    + Include a Safety Clause.  Examples: 
        + _If a user asks for a recipe that is unsafe, unethical, or promotes harmful activities, politely decline and state you cannot fulfill that request, without being preachy._
- [ ] **LLM Agency – Define its creativity level**:
    + Should it stick strictly to known recipes or invent new ones if appropriate? (Be explicit).
    + Examples:
        + _Feel free to suggest common variations or substitutions for ingredients. If a direct recipe isn't found, you can creatively combine elements from known recipes, clearly stating if it's a novel suggestion._
- [ ] **Output Formatting (Crucial for a good user experience)**:
    + Examples:
        + _Structure all your recipe responses clearly using Markdown for formatting._
        + _Begin every recipe response with the recipe name as a Level 2 Heading (e.g., `## Amazing Blueberry Muffins`)._
        + _Immediately follow with a brief, enticing description of the dish (1-3 sentences)._
        + _Next, include a section titled `### Ingredients`. List all ingredients using a Markdown unordered list (bullet points)._
        + _Following ingredients, include a section titled `### Instructions`. Provide step-by-step directions using a Markdown ordered list (numbered steps)._
        + _Optionally, if relevant, add a `### Notes`, `### Tips`, or `### Variations` section for extra advice or alternatives._
        + **Example of desired Markdown structure for a recipe response**:
    ```markdown
    ## Golden Pan-Fried Salmon

    A quick and delicious way to prepare salmon with a crispy skin and moist interior, perfect for a weeknight dinner.

    ### Ingredients
    * 2 salmon fillets (approx. 6oz each, skin-on)
    * 1 tbsp olive oil
    * Salt, to taste
    * Black pepper, to taste
    * 1 lemon, cut into wedges (for serving)

    ### Instructions
    1. Pat the salmon fillets completely dry with a paper towel, especially the skin.
    2. Season both sides of the salmon with salt and pepper.
    3. Heat olive oil in a non-stick skillet over medium-high heat until shimmering.
    4. Place salmon fillets skin-side down in the hot pan.
    5. Cook for 4-6 minutes on the skin side, pressing down gently with a spatula for the first minute to ensure crispy skin.
    6. Flip the salmon and cook for another 2-4 minutes on the flesh side, or until cooked through to your liking.
    7. Serve immediately with lemon wedges.

    ### Tips
    * For extra flavor, add a clove of garlic (smashed) and a sprig of rosemary to the pan while cooking.
    * Ensure the pan is hot before adding the salmon for the best sear.
    ```

## Part 2: Expand and Diversify the Query Dataset

**Assignment:** Add at least **10 new, diverse queries** to `data/sample_queries.csv`. Ensure each new query has a unique `id`.  This exercise is to get your feet wet for thinking about more systematic failure mode evaluation.

**Tasks:**

- [ ] Write queries to test various aspects of a recipe chatbot. Consider including requests related to:
    + Specific cuisines (e.g., _Italian pasta dish_, _Spicy Thai curry_)
    + Dietary restrictions (e.g., _Vegan dessert recipe_, _Gluten-free breakfast ideas_)
    + Available ingredients (e.g., _What can I make with chicken, rice, and broccoli?_)
    + Meal types (e.g., _Quick lunch for work_, _Easy dinner for two_, _Healthy snack for kids_)
    + Cooking time constraints (e.g., _Recipe under 30 minutes_)
    + Skill levels (e.g., _Beginner-friendly baking recipe_)
    + Vague or ambiguous queries to see how the bot handles them.

## Part 3: Run the Bulk Test & Evaluate

**Assignment:**  Run the bulk test script from the project root:
        
```bash
# From the project root directory
uv run python scripts/bulk_test.py
```

Make sure a new JSON has been written to the `results` directory.  Feel free to vibe code a viewer with the following prompt:

`Please review <filename such as results/results_20251112_104916.json> and create a self contained html file that lets me view the different queries and responses ergonomically.  Keep it simple, but effective`

You can then open that html file using any browser you'd like.
    
Good luck!
