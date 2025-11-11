"""
Program Management Knowledge Agent - Starter Code

This program demonstrates two approaches to answering program management questions:
1. Using hardcoded knowledge
2. Using an LLM API

Complete the TODOs to build your knowledge agent.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(
    #base_url = "https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

def get_hardcoded_answer(question):
    """
    Return answers to program management questions using hardcoded knowledge.
    
    Args:
        question (str): The question about program management
        
    Returns:
        str: The answer to the question
    """
    # Convert question to lowercase for easier matching 
    question = question.lower()

    # Knowledge base for program management questions
    knowledge_base = {
        "gantt": """A Gantt chart is a visual project management tool that displays project tasks and activities against a timeline. It shows:
- Task start and end dates
- Task dependencies (which tasks must be completed before others can start)
- Current progress of each task
- Overall project timeline and milestones
- Resource allocation across tasks

Gantt charts are particularly useful for planning, tracking progress, identifying critical path activities, and communicating project status to stakeholders.""",
        
        "agile": """Agile is an iterative and incremental project management methodology that emphasizes:
- Flexibility and adaptability to changing requirements
- Close collaboration between cross-functional teams
- Delivering working software in short iterations (typically 2-4 weeks)
- Continuous customer feedback and improvement
- Emphasis on individuals and interactions over processes and tools

Key Agile principles include customer satisfaction through early delivery, welcoming changing requirements, and delivering working software frequently. Common Agile frameworks include Scrum, Kanban, and Extreme Programming (XP).""",
        
        "sprint": """A sprint is a fixed time period (typically 1-4 weeks) during which a development team works to complete a set of planned work items. Key characteristics:
- Fixed duration (usually 2 weeks)
- Sprint planning meeting at the start to select work items
- Daily stand-up meetings to track progress
- Sprint review/demo at the end to showcase completed work
- Sprint retrospective to improve the process

During a sprint, the team commits to completing specific user stories or tasks, and no changes are made to the sprint goal. Benefits include providing regular rhythm, enabling quick feedback, and breaking large projects into manageable chunks.""",
        
        "critical path": """The critical path is the longest sequence of dependent tasks in a project that determines the minimum project duration. Key points:
- Any delay in critical path activities will delay the entire project
- The critical path has zero float/slack (no room for delays)
- It's calculated using the Critical Path Method (CPM)

To identify the critical path:
1. List all project activities and their durations
2. Identify dependencies between activities
3. Calculate earliest start/finish times (forward pass)
4. Calculate latest start/finish times (backward pass)
5. Activities with zero float are on the critical path

This helps prioritize resources on the most important activities and enables better risk management.""",
        
        "milestone": """A milestone is a significant point or event in a project that marks the completion of a major phase or deliverable. Characteristics:
- Represents a key achievement or decision point
- Has zero duration (it's a point in time, not a task)
- Often requires approval or sign-off before proceeding
- Used to track progress and measure success

Common types of milestones include phase completion, major deliverables, key decision points, external dependencies, and contractual obligations. Benefits include providing clear progress checkpoints, enabling better communication with stakeholders, and supporting risk management."""
    }
    
    # Check if the question contains any of the knowledge base keywords
    for keyword, answer in knowledge_base.items():
        if keyword in question:
            return answer
    
    # Default response for questions not in the knowledge base
    return "I'm sorry, I don't have information about that specific program management topic in my knowledge base. I can answer questions about: Gantt charts, Agile methodology, sprints, critical path, and milestones."

def get_llm_answer(question):
    """
    Get answers to program management questions using an LLM API.
    
    Args:
        question (str): The question about program management
        
    Returns:
        str: The answer from the LLM
    """
    # Check if the LLM client is initialized
    if client is None:
        return "Error: LLM client is not initialized."
    
    try:
        # Implement the API call to get an answer from the LLM
        # Use a system message to specify that the LLM should act as a program management expert
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert program management consultant with extensive knowledge of project management methodologies, tools, and best practices. Provide clear, concise, and accurate answers to program management questions."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7
        )
        
        # Extract and return the answer
        answer = response.choices[0].message.content.strip()
        return answer
        
    except Exception as e:
        # Add error handling for API calls
        return f"Error getting answer from LLM: {str(e)}"

# Demo function to compare both approaches
def compare_answers(question):
    """Compare answers from both approaches for a given question."""
    print(f"\nQuestion: {question}")
    print("-" * 50)
    
    # Get and display the hardcoded answer
    print("\n[Hardcoded Answer]")
    hardcoded_answer = get_hardcoded_answer(question)
    print(hardcoded_answer)
    
    # Get and display the LLM answer (or a placeholder message)
    print("\n[LLM Answer]")
    llm_answer = get_llm_answer(question)
    print(llm_answer)
    
    print("=" * 50)

# Demo with sample questions
if __name__ == "__main__":
    print("PROGRAM MANAGEMENT KNOWLEDGE AGENT DEMO")
    print("=" * 50)
    
    # Create a list of sample program management questions
    sample_questions = [
        "What is a Gantt chart?",
        "Can you explain Agile methodology?",
        "What are sprints in project management?",
        "Tell me about the critical path method",
        "What is a milestone in project management?"
    ]
    
    # Loop through the questions and compare answers
    for question in sample_questions:
        compare_answers(question)