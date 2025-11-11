import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(
    #base_url = "https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

MAX_RETRIES = 5

def llm_call(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Basic LLM call wrapper."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def extract_xml(text: str, tag: str) -> str:
    """Extract content between XML-style tags."""
    pattern = rf"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

# Recipe Optimizer class
class RecipeOptimizer:
    def __init__(self, base_dish, constraints):
        self.base_dish = base_dish
        self.constraints = constraints

    def run(self):
        constraints_str = "\n".join([f"- {constraint}" for constraint in self.constraints])
        prompt = f"""You are a recipe optimizer. Your task is to optimize the base dish "{self.base_dish}" based on the following user constraints:

{constraints_str}

Return your response in the following format:
<response>
- <recipe>
- <ingredients>
- <instructions>
- <nutrition>
- <calories>
- <protein>
- <user-rating>
- <user-comments>
</response>
"""
        raw_output = llm_call(prompt)
        print("\n[Raw Recipe Optimizer Output]\n", raw_output)
        result = extract_xml(raw_output, "response")
        return result

# Example user constraints
RECIPE_REQUEST = {
    "base_dish": "pasta",
    "constraints": [
        "gluten-free",
        "vegan",
        "under 500 calories per serving",
        "high protein (>15g per serving)",
        "no tomatoes",
        "taste must be rated 9/10 or higher"
    ]
}
# Evaluator Agent class
class EvaluatorAgent:
    def __init__(self, recipe, constraints):
        self.recipe = recipe
        self.constraints = constraints

    def run(self):
        constraints_str = "\n".join([f"- {constraint}" for constraint in self.constraints])
        prompt = f"""You are a recipe evaluator. Your task is to evaluate the following recipe to check if it meets the user constraints.

Recipe:
{self.recipe}

User Constraints:
{constraints_str}

Give a rating between 1 and 10 for the recipe based on how well it meets these constraints.
Return your response in the following format:
<response>
<rating>8</rating>
<comments>Your comments here</comments>
</response>
"""
        raw_output = llm_call(prompt)
        print("\n[Raw Evaluator Agent Output]\n", raw_output)
        response_text = extract_xml(raw_output, "response")
        
        # Extract rating and comments from the response
        rating_text = extract_xml(response_text, "rating")
        comments_text = extract_xml(response_text, "comments")
        
        # Try to extract numeric rating from the text
        rating_match = re.search(r'\d+', rating_text)
        rating = int(rating_match.group()) if rating_match else 0
        
        return {
            "rating": rating,
            "comments": comments_text
        }


if __name__ == "__main__":
    # Continue evaluating the recipe using evaluator agent for 5 tries
    for i in range(5):
        recipe_optimizer = RecipeOptimizer(RECIPE_REQUEST["base_dish"], RECIPE_REQUEST["constraints"])
        result = recipe_optimizer.run()
        print("\n[Recipe Optimizer Result]\n", result)
        
        evaluator_agent = EvaluatorAgent(result, RECIPE_REQUEST["constraints"])
        evaluator_result = evaluator_agent.run()
        print("\n[Evaluator Agent Result]\n", evaluator_result)
        print(f"Rating: {evaluator_result['rating']}/10")
        print(f"Comments: {evaluator_result['comments']}")
        
        if evaluator_result["rating"] >= 9:
            print("Recipe meets constraints. Exiting...")
            break
        else:
            print(f"Recipe did not meet constraints. Retrying... ({i+1}/5)")
    else:
        print("Failed to meet constraints after 5 tries. Please try again.")
   