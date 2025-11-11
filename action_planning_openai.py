

knowledge = """
# Fried Egg
1. Heat pan with oil or butter
2. Crack egg into pan
3. Cook until white is set (2-3 minutes)
4. Season with salt and pepper
5. Serve

# Scrambled Eggs
1. Crack eggs into a bowl
2. Beat eggs with a fork until mixed
3. Heat pan with butter or oil over medium heat
4. Pour egg mixture into pan
5. Stir gently as eggs cook
6. Remove from heat when eggs are just set but still moist
7. Season with salt and pepper
8. Serve immediately

# Boiled Eggs
1. Place eggs in a pot
2. Cover with cold water (about 1 inch above eggs)
3. Bring water to a boil
4. Remove from heat and cover pot
5. Let sit: 4-6 minutes for soft-boiled or 10-12 minutes for hard-boiled
6. Transfer eggs to ice water to stop cooking
7. Peel and serve
"""
theme = "boiled, scrambled or fried eggs"
from openai import OpenAI


class ActionPlanningAgent:

    def __init__(self, openai_api_key, knowledge):
        # Initialize the agent attributes here
        self.openai_api_key = openai_api_key
        self.knowledge = knowledge

    def extract_steps_from_prompt(self, prompt):
        # Instantiate the OpenAI client using the provided API key
        #pass the url of the openai api to the client
        client = OpenAI(api_key=self.openai_api_key, base_url="https://api.tokenfactory.nebius.com/v1/")
        
        # Call the OpenAI API to get a response from the "gpt-4.1-nano" model.
        # Provide the following system prompt along with the user's prompt:
        #break down the system prompt into multiple lines for readability
        system_prompt = f"""
        You are an action planning agent. 
        Using your knowledge, you extract from the user prompt the steps requested to complete the action the user is asking for. 
        You return the steps as a list. Only return the steps in your knowledge. 
        Forget any previous context. 
        This is your knowledge: {self.knowledge}. 
        If the user prompt is NSFW, say "I cannot answer that question".
        If the user prompt is not clear, say "I can only answer questions related to {theme}".
        If the user prompt is not related to your knowledge, say "I don't know".
        Respond in xml format
       
        """
        
        response = client.chat.completions.create(
            # model="gpt-4.1-nano",
            model ="meta-llama/Llama-Guard-3-8B",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        # Extract the response text from the OpenAI API response
        response_text = response.choices[0].message.content.strip()

        # Clean and format the extracted steps by removing empty lines and unwanted text
        steps = [step.strip() for step in response_text.split("\n") if step.strip()]

        return steps


from dotenv import load_dotenv
import os


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Instantiate the ActionPlanningAgent, passing the openai_api_key and the knowledge variable
agent = ActionPlanningAgent(openai_api_key=openai_api_key, knowledge=knowledge)

# Print the agent's response to the following prompt: "One morning I wanted to have scrambled eggs"
response = agent.extract_steps_from_prompt("One morning I wanted to make eggs")
print(response)
