<!-- for HW 2: Template for defining failure mode taxonomy -->

# Failure Mode Taxonomy

This document outlines the failure modes observed or anticipated for the Recipe Chatbot. Each failure mode includes a title, a concise definition, and illustrative examples.

## Failure Mode 1: Missing Serving Size Information

*   **Definition**: Bot fails to specify the number of servings or portion sizes in the recipe.
*   **Illustrative Examples**:
    1.  *User Query*: "Quick egg spinach cheese recipe pls"
        *Bot Response*: Provides recipe with ingredients like "2 large eggs, 1 cup fresh spinach" without specifying how many people this serves.
    2.  *User Query*: "What's a simple recipe using salmon lemon and fresh herbs"
        *Bot Response*: Lists "2 salmon fillets" without indicating if this is for one or multiple servings.
    3.  *User Query (SYN001)*: "need easy dairy free curry recipes"
        *Bot Response*: Provides "Easy Dairy-Free Chicken Curry" with "1 lb (450g) boneless, skinless chicken breasts or thighs" without specifying the number of servings.

## Failure Mode 2: Overcomplicated Simple Recipes

*   **Definition**: Bot provides recipes with too many ingredients or steps for what should be a simple dish.
*   **Illustrative Examples**:
    1.  *User Query*: "quick egg spinach cheese recipe pls"
        *Bot Response*: Includes optional ingredients like garlic powder, red pepper flakes, and multiple preparation steps that could be simplified.
    2.  *User Query*: "simple recipe using salmon lemon and fresh herbs"
        *Bot Response*: Provides complex marinade preparation and multiple cooking methods (baking and pan-frying) when a simpler approach would suffice.
    3.  *User Query (SYN021)*: "quick egg spinach cheese recipe pls"
        *Bot Response*: For "Creamy Egg, Spinach, and Cheese Scramble," includes "Optional: a pinch of garlic powder or red pepper flakes for extra flavor," adding potential complexity and time to a request for a "quick" recipe.

## Failure Mode 3: Inconsistent Time Estimates

*   **Definition**: Bot provides recipes that don't match the requested time constraints or includes preparation time inaccurately.
*   **Illustrative Examples**:
    1.  *User Query*: "Whatcha got for a 30 min eggs and cheese dinner?"
        *Bot Response*: Suggests a recipe that requires toasting, cooking meat, and multiple steps that would likely exceed 30 minutes.
    2.  *User Query*: "quick salmon dinner ideas"
        *Bot Response*: Includes 10-15 minute marination time in a "quick" recipe.
    3.  *User Query (SYN018)*: "Looking for quick salmon dinner ideas with lemon and herbs pls!"
        *Bot Response*: For "Lemon Herb Salmon," states it can be enjoyed in "about 20 minutes" but includes a step to "Let it marinate for at least 10 minutes," which, combined with prep and cooking time, could make the "quick" estimate misleading for some users.

## Failure Mode 4: Missing Dietary Restriction Information

*   **Definition**: Bot fails to properly address or verify dietary restrictions in the recipe.
*   **Illustrative Examples**:
    1.  *User Query*: "low FODMAP recipe"
        *Bot Response*: Suggests using ingredients like "gluten-free wrap" without verifying if it's actually low FODMAP.
    2.  *User Query*: "pescatarian dishes"
        *Bot Response*: Suggests using store-bought pesto without checking if it contains non-pescatarian ingredients.
    3.  *User Query (SYN020)*: "got any pescatarian dishes I can make with salmon that won't take long thx!"
        *Bot Response*: Suggests "Pesto Salmon Fillet" using "store-bought or homemade" pesto without advising the user to check store-bought pesto for non-pescatarian ingredients (like cheese containing animal rennet).
    4.  *User Query (SYN008)*: "What's a quick and easy recipe I can make with pantry ingredients that follows low FODMAP diet?"
        *Bot Response*: For "Lemon Herb Quinoa," suggests ingredients like "dried oregano or thyme (check for FODMAP content)," placing the burden of verification for the dietary restriction on the user.

## Failure Mode 5: Incomplete Ingredient Substitutions

*   **Definition**: Bot fails to provide alternative ingredients or substitutions for common dietary restrictions or preferences.
*   **Illustrative Examples**:
    1.  *User Query*: "low FODMAP recipe"
        *Bot Response*: Doesn't provide alternatives for ingredients that might be high in FODMAPs.
    2.  *User Query*: "quick egg spinach cheese recipe"
        *Bot Response*: Doesn't suggest dairy-free alternatives for the cheese component.
    3.  *User Query (SYN021)*: "quick egg spinach cheese recipe pls"
        *Bot Response*: For "Creamy Egg, Spinach, and Cheese Scramble," uses "shredded cheese" but does not suggest dairy-free alternatives for users who might need or prefer them.

## Failure Mode 6: Inconsistent Recipe Formatting

*   **Definition**: Bot provides recipes with inconsistent formatting, making it difficult to follow instructions or understand ingredient quantities.
*   **Illustrative Examples**:
    1.  *User Query*: "quick salmon dinner ideas"
        *Bot Response*: Mixes metric and imperial measurements without conversion (e.g., "400°F" and "2 tablespoons").
    2.  *User Query*: "low FODMAP recipe"
        *Bot Response*: Inconsistently formats ingredient lists and steps, making it harder to follow.
    3.  *User Query (SYN021)*: "quick egg spinach cheese recipe pls"
        *Bot Response*: For "Creamy Egg, Spinach, and Cheese Scramble," specifies using a "non-stick skillet" without suggesting alternatives if the user doesn't have one available.

## Failure Mode 7: Missing Equipment Requirements

*   **Definition**: Bot fails to specify necessary cooking equipment or assumes availability of specific tools.
*   **Illustrative Examples**:
    1.  *User Query*: "quick egg spinach cheese recipe"
        *Bot Response*: Mentions using a non-stick skillet without suggesting alternatives.
    2.  *User Query*: "simple salmon recipe"
        *Bot Response*: Requires a grill or grill pan without providing stovetop alternatives.
    3.  *User Query (SYN021)*: "quick egg spinach cheese recipe pls"
        *Bot Response*: For "Creamy Egg, Spinach, and Cheese Scramble," specifies using a "non-stick skillet" without suggesting alternatives if the user doesn't have one available.

## Failure Mode 8: Inadequate Safety Information

*   **Definition**: Bot fails to provide important safety information or cooking temperature guidelines. I guess generally, we want to have good cooking temperature guidelines.
*   **Illustrative Examples**:
    1.  *User Query*: "quick salmon dinner ideas"
        *Bot Response*: Doesn't mention safe internal temperature for cooked salmon.
    2.  *User Query (SYN012)*: "need to impress my friends with a complex dish like a keto casserole something with meat and veggies would be great"
        *Bot Response*: For "Beef Cauliflower Bake" (containing ground beef), the bot instructs to cook ground beef "until browned and cooked through" before incorporating it into a casserole and baking. It omits the explicit guideline to cook ground beef to an internal temperature of 160°F (71°C), which is an important safety measure, especially for a "complex dish."
