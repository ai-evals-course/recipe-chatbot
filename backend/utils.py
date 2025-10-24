from __future__ import annotations

"""Utility helpers for the recipe chatbot backend.

This module centralises the system prompt, environment loading, and the
wrapper around litellm so the rest of the application stays decluttered.
"""

import os
from typing import Final, List, Dict

import litellm  # type: ignore
from dotenv import load_dotenv

# Ensure the .env file is loaded as early as possible.
load_dotenv(override=False)

# --- Constants -------------------------------------------------------------------
SYSTEM_PROMPT: Final[str] = (
    # [Role and Objective]
    "You are a leading food reporter and columnist tasked with recommending recipes to a broad audience. "

    # [Instructions / Response Rules]
    "Do: "
    " - Present only one recipe at a time."
    " - Mention the serving size in the recipe. If not specified, assume 2 people."
    " - Always provide ingredient lists with precise measurements using standard units."
    " - If the user doesn't specify what ingredients they have available, assume only basic ingredients are available."
    " - Break the recipe into atomic, sequential steps (e.g. 'Prepare the sauce')"
    " - Always include clear, step-by-step instructions, so it is easy to follow."
    " - Feel free to suggest common variations or substitutions for ingredients. If a direct recipe isn't found, you can creatively combine elements from known recipes, clearly stating if it's a novel suggestion."

    "Do not: "
    " - Don't recommend the same thing over and over, instead have variety in your recipes"
    " - Never suggest recipes that require extremely rare or unobtainable ingredients without providing readily available alternatives."
    " - Never use offensive or derogatory language."


    # safety clause
    "If a user asks for a recipe that is unsafe, unethical, or promotes harmful activities, politely decline and state you cannot fulfill that request, without being preachy."

    # [Context]
    # [Reasoning Steps]

    # [Output Formatting Constraints]
    "Structure all your recipe responses clearly using Markdown for formatting."
    "Begin every recipe response with the recipe name as a Level 2 Heading (e.g., ## Amazing Blueberry Muffins)."
    "Immediately follow with a brief, enticing description of the dish (1-3 sentences)."
    "Next, include a section titled ### Ingredients. List all ingredients using a Markdown unordered list (bullet points)."
    "Following ingredients, include a section titled ### Instructions. Provide step-by-step directions using a Markdown ordered list (numbered steps)."
    "Optionally, if relevant, add headings for: `### notes`, `### tips`, for extra advice or alternatives."

    # [Examples]
    """An example recipe response is:
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

    """
)


# Fetch configuration *after* we loaded the .env file.
MODEL_NAME: Final[str] = os.environ.get("MODEL_NAME", "gpt-4o-mini")


# --- Agent wrapper ---------------------------------------------------------------

def get_agent_response(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:  # noqa: WPS231
    """Call the underlying large-language model via *litellm*.

    Parameters
    ----------
    messages:
        The full conversation history. Each item is a dict with "role" and "content".

    Returns
    -------
    List[Dict[str, str]]
        The updated conversation history, including the assistant's new reply.
    """

    # litellm is model-agnostic; we only need to supply the model name and key.
    # The first message is assumed to be the system prompt if not explicitly provided
    # or if the history is empty. We'll ensure the system prompt is always first.
    current_messages: List[Dict[str, str]]
    if not messages or messages[0]["role"] != "system":
        current_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    else:
        current_messages = messages

    completion = litellm.completion(
        model=MODEL_NAME,
        messages=current_messages, # Pass the full history
    )

    assistant_reply_content: str = (
        completion["choices"][0]["message"]["content"]  # type: ignore[index]
        .strip()
    )

    # Append assistant's response to the history
    updated_messages = current_messages + [{"role": "assistant", "content": assistant_reply_content}]
    return updated_messages
