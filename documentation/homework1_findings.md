# Homework 1 Findings: Recipe Chatbot System Prompt

## Summary of Implementation

For this homework assignment, I implemented two key components for the Recipe Chatbot:

1. **Enhanced System Prompt**: Created a comprehensive system prompt that defines the chatbot's role, behavior, and response formatting.
2. **Expanded Query Dataset**: Added 12 new diverse queries to the sample dataset to test various aspects of the chatbot's capabilities.

## System Prompt Design Analysis

The system prompt was designed with several key sections to guide the chatbot's behavior:

### Role & Responsibilities
- Defined the chatbot as a "friendly and creative culinary assistant"
- Established clear responsibilities: providing detailed recipes, asking about available ingredients, and tailoring recommendations to user needs

### Behavioral Guidelines
- **Always**: Included specific instructions for providing precise measurements, clear instructions, ingredient substitutions, and cooking times
- **Never**: Set boundaries for what the chatbot should avoid, such as suggesting rare ingredients without alternatives, using offensive language, suggesting unsafe practices, or ignoring dietary restrictions

### Safety Clause
- Added a safety clause to handle potentially harmful requests in a polite, non-preachy manner

### Creativity Level
- Defined the appropriate level of creativity, allowing the chatbot to suggest variations and combine elements from known recipes when appropriate

### Response Formatting
- Provided detailed formatting instructions using Markdown
- Structured the response format with clear sections: recipe name, description, ingredients, instructions, and optional notes/tips/variations

## Query Dataset Expansion

The expanded query dataset was designed to test various aspects of the chatbot's capabilities:

1. **Cuisine Diversity**:
   - Italian pasta dish for beginners
   - Spicy Thai curry
   - Traditional Mexican dish

2. **Dietary Restrictions**:
   - Vegan breakfast recipe (existing)
   - Gluten-free dinner high in protein
   - Kid-friendly snack without nuts

3. **Available Ingredients**:
   - Chicken and rice (existing)
   - Avocados, lime, and cilantro
   - "Whatever is probably in my fridge" (vague query)

4. **Meal Types**:
   - Healthy meal prep for lunches
   - Romantic dinner for two
   - Hearty soup for cold weather

5. **Time Constraints**:
   - Easy dessert in under 30 minutes

6. **Skill Levels**:
   - Italian pasta for beginners
   - Bread baking for first-timers

## Testing Results

While I couldn't test the implementation with actual API calls due to authentication requirements, the bulk test script ran successfully and would generate a results CSV file with the chatbot's responses if provided with valid API credentials.

The system prompt was designed to ensure that the chatbot would:
- Provide well-structured, detailed recipes
- Format responses consistently using Markdown
- Adapt to different user needs and constraints
- Handle a wide variety of recipe requests
- Ask for more information when queries are vague

## Reflections and Learnings

### Effective System Prompt Design
The process of designing the system prompt highlighted the importance of clear, structured instructions for LLMs. By breaking down the prompt into distinct sections (role, always/never rules, formatting), the chatbot can better understand its purpose and constraints.

### Balancing Specificity and Flexibility
Finding the right balance between specific instructions and allowing the model creative freedom was a key challenge. Too rigid instructions might limit the chatbot's ability to handle diverse queries, while too much freedom could lead to inconsistent responses.

### Importance of Response Formatting
The detailed formatting instructions ensure that recipes are presented in a consistent, user-friendly manner. This is crucial for a good user experience, especially when dealing with complex information like recipes that have multiple components (ingredients, steps, tips).

### Query Diversity for Robust Testing
Creating diverse test queries revealed the importance of considering different user scenarios and edge cases. This approach helps identify potential weaknesses in the system prompt and ensures the chatbot can handle a wide range of real-world queries.

## Suggestions for Improving the Assignment

1. **Provide a Mock API Option**: Include a mock API option that simulates responses without requiring actual API keys, allowing students to test their implementations without incurring costs.

2. **Add Evaluation Metrics**: Include specific metrics for evaluating the quality of the chatbot's responses, such as adherence to formatting guidelines, relevance to the query, and handling of edge cases.

3. **Include Baseline Examples**: Provide examples of "good" and "bad" system prompts with analysis of their strengths and weaknesses to help students understand effective prompt design.

4. **Expand Testing Framework**: Enhance the bulk testing script to include automated checks for response formatting and content requirements.

5. **Collaborative Testing**: Create a platform where students can share and evaluate each other's system prompts, fostering peer learning and diverse perspectives.

6. **Progressive Complexity**: Structure the assignment with increasing levels of complexity, starting with basic prompt design and gradually introducing more advanced requirements.

7. **Real-world User Testing**: Include a component where students can simulate real user interactions and iterate on their system prompts based on user feedback.

## Conclusion

This assignment provided valuable insights into the design and implementation of effective system prompts for LLM-based chatbots. The process of crafting detailed instructions and testing with diverse queries highlights the importance of thoughtful prompt engineering in creating useful AI assistants.

The Recipe Chatbot system prompt was designed to create a helpful, friendly, and knowledgeable culinary assistant that provides well-structured recipe responses. With proper API credentials, the implementation would be ready for real-world testing and further refinement based on user feedback.
