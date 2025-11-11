

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
import google.generativeai as genai


class ActionPlanningAgent:

    def __init__(self, gemini_api_key, knowledge, model_name='gemma-3-27b-it'):
        # Initialize the agent attributes here
        self.gemini_api_key = gemini_api_key
        self.knowledge = knowledge
        self.model_name = model_name
        # Configure Gemini API
        genai.configure(api_key=self.gemini_api_key)
    
    def list_available_models(self):
        """Helper method to list all available Gemini models"""
        try:
            models = genai.list_models()
            print("Available Gemini models:")
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    print(f"  - {model.name}")
        except Exception as e:
            print(f"Error listing models: {e}")

    def extract_steps_from_prompt(self, prompt):
        # Instantiate the Gemini model
        # Default is 'gemini-pro' (most commonly available)
        # If model not found, call agent.list_available_models() to see available options
        model = genai.GenerativeModel(self.model_name)
        
        # Create the system prompt and combine with user prompt
        # Gemini combines system and user prompts into a single prompt
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
        
        # Combine system prompt and user prompt for Gemini
        full_prompt = f"{system_prompt}\n\nUser prompt: {prompt}"
        
        # Generate content using Gemini
        response = model.generate_content(
            full_prompt,
            generation_config={
                'temperature': 0.2
            }
        )
        
        # Extract the response text from the Gemini API response
        response_text = response.text.strip()

        # Clean and format the extracted steps by removing empty lines and unwanted text
        steps = [step.strip() for step in response_text.split("\n") if step.strip()]

        return steps


from dotenv import load_dotenv
import os


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Instantiate the ActionPlanningAgent, passing the gemini_api_key and the knowledge variable
agent = ActionPlanningAgent(gemini_api_key=gemini_api_key, knowledge=knowledge)
agent.list_available_models()
# Print the agent's response to the following prompt: "One morning I wanted to have scrambled eggs"
response = agent.extract_steps_from_prompt("One morning I wanted to make eggs")
print(response)
