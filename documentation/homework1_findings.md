# Homework 1: Findings

## Overview

During this exercise, I explored different strategies to improve the process of prompt engineering and model evaluation. Below are the key findings and insights gained from the experience.

## Automated Prompt Testing

One of the most valuable discoveries was the effectiveness of using a script to test prompts with multiple queries. This approach significantly streamlined the workflow, enabling rapid iteration and refinement of prompts. By automating the testing process, I was able to:

- Quickly identify weaknesses or ambiguities in the prompt.
- Compare model responses across a variety of scenarios.
- Save time and reduce manual effort in evaluating prompt performance.

## Model Selection and Performance

Initially, I used the `openai/gpt-4.1-nano` model for testing. However, I observed that this model struggled to handle certain instructions and often failed to produce the desired results. To address this, I switched to the `openai/gpt-4.1-mini` model, which demonstrated improved comprehension and response quality for the same set of queries.

This experience highlighted the importance of selecting the appropriate model for the task, as even small differences in model capabilities can have a significant impact on outcomes.

## Further Analysis

For a more detailed analysis of the findings and additional insights, please refer to [exercise_analysis.md](exercise_analysis.md).