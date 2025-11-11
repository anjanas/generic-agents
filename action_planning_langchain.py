

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
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# LangChain provides a unified interface for LLM providers:
# - OpenAI, Anthropic, Google, Cohere, and more
# - Custom OpenAI-compatible endpoints (like Nebius Token Factory)
# - Built-in support for chains, agents, and memory


class ActionPlanningAgent:

    def __init__(self, api_key, knowledge, model_name, api_base="https://api.tokenfactory.nebius.com/v1/"):
        # Initialize the agent attributes here
        self.api_key = api_key
        self.knowledge = knowledge
        self.model_name = model_name
        self.api_base = api_base
        
        # Initialize LangChain ChatOpenAI with custom base URL for OpenAI-compatible endpoints
        # Remove 'openai/' prefix from model name if present
        model_name_clean = model_name.replace("openai/", "") if model_name.startswith("openai/") else model_name
        
        self.llm = ChatOpenAI(
            model=model_name_clean,
            api_key=self.api_key,
            base_url=self.api_base,
            temperature=0.2
        )

    def extract_steps_from_prompt(self, prompt):
        # LangChain provides a unified interface for LLM providers
        # It supports OpenAI-compatible APIs with custom base URLs
        
        # Create the system prompt
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
        
        # Use LangChain to call the API with custom base URL
        # LangChain uses SystemMessage and HumanMessage for structured prompts
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
        ]
        
        # Invoke the LLM with the messages
        response = self.llm.invoke(messages)
        
        # Extract the response text from LangChain response
        response_text = response.content.strip()

        # Clean and format the extracted steps by removing empty lines and unwanted text
        steps = [step.strip() for step in response_text.split("\n") if step.strip()]

        return steps


from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Instantiate the ActionPlanningAgent using LangChain
# LangChain supports multiple providers and custom OpenAI-compatible endpoints
agent = ActionPlanningAgent(
    api_key=api_key, 
    knowledge=knowledge,
    model_name="moonshotai/Kimi-K2-Instruct",  # Using model from Nebius Token Factory
    # Alternative: "gpt-oss-20b" or "gpt-oss-120b" for GPT-OSS models
    api_base="https://api.tokenfactory.nebius.com/v1/"  # Nebius Token Factory endpoint
)

# Print the agent's response to the following prompt: "One morning I wanted to have scrambled eggs"
response = agent.extract_steps_from_prompt("One morning I wanted to make fried eggs")
print(response)
