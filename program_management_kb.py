# Program Management Knowledge Base
# Responses for common program management questions

PROGRAM_MANAGEMENT_KB = {
    "gantt chart": {
        "question": "What is a Gantt chart?",
        "answer": """A Gantt chart is a visual project management tool that displays project tasks and activities against a timeline. It shows:
- Task start and end dates
- Task dependencies (which tasks must be completed before others can start)
- Current progress of each task
- Overall project timeline and milestones
- Resource allocation across tasks

Gantt charts are particularly useful for:
- Planning and scheduling projects
- Tracking progress
- Identifying critical path activities
- Communicating project status to stakeholders
- Managing dependencies between tasks"""
    },
    
    "agile": {
        "question": "What is Agile methodology?",
        "answer": """Agile is an iterative and incremental project management methodology that emphasizes:
- Flexibility and adaptability to changing requirements
- Close collaboration between cross-functional teams
- Delivering working software in short iterations (typically 2-4 weeks)
- Continuous customer feedback and improvement
- Emphasis on individuals and interactions over processes and tools

Key Agile principles:
- Customer satisfaction through early and continuous delivery
- Welcome changing requirements
- Deliver working software frequently
- Business people and developers work together daily
- Build projects around motivated individuals
- Working software is the primary measure of progress

Common Agile frameworks include Scrum, Kanban, and Extreme Programming (XP)."""
    },
    
    "sprint": {
        "question": "What is a sprint in Agile?",
        "answer": """A sprint is a fixed time period (typically 1-4 weeks) during which a development team works to complete a set of planned work items. Key characteristics:
- Fixed duration (usually 2 weeks)
- Sprint planning meeting at the start to select work items
- Daily stand-up meetings to track progress
- Sprint review/demo at the end to showcase completed work
- Sprint retrospective to improve the process

During a sprint:
- The team commits to completing specific user stories or tasks
- No changes are made to the sprint goal during the sprint
- Team focuses solely on sprint backlog items
- Progress is tracked daily

Benefits of sprints:
- Provides regular rhythm and predictability
- Allows for quick feedback and adaptation
- Breaks large projects into manageable chunks
- Enables continuous delivery of value"""
    },
    
    "critical path": {
        "question": "What is the critical path in project management?",
        "answer": """The critical path is the longest sequence of dependent tasks in a project that determines the minimum project duration. Key points:
- Any delay in critical path activities will delay the entire project
- The critical path has zero float/slack (no room for delays)
- It's calculated using the Critical Path Method (CPM)

How to identify the critical path:
1. List all project activities and their durations
2. Identify dependencies between activities
3. Calculate earliest start/finish times (forward pass)
4. Calculate latest start/finish times (backward pass)
5. Activities with zero float are on the critical path

Benefits:
- Identifies tasks that must be completed on time
- Helps prioritize resources on most important activities
- Shows which tasks can be delayed without affecting project completion
- Enables better risk management by focusing on critical activities

Management implications:
- Monitor critical path activities closely
- Allocate best resources to critical path tasks
- Have contingency plans for critical path delays"""
    },
    
    "milestone": {
        "question": "What is a milestone in project management?",
        "answer": """A milestone is a significant point or event in a project that marks the completion of a major phase or deliverable. Characteristics:
- Represents a key achievement or decision point
- Has zero duration (it's a point in time, not a task)
- Often requires approval or sign-off before proceeding
- Used to track progress and measure success

Common types of milestones:
- Phase completion (e.g., "Design Phase Complete")
- Major deliverable (e.g., "First Prototype Delivered")
- Key decision points (e.g., "Go/No-Go Decision")
- External dependencies (e.g., "Client Approval Received")
- Contractual obligations (e.g., "Payment Milestone 1")

Benefits:
- Provides clear progress checkpoints
- Helps with project planning and scheduling
- Enables better communication with stakeholders
- Facilitates resource planning
- Supports risk management by identifying critical checkpoints

Best practices:
- Set milestones at meaningful project points
- Make milestones measurable and specific
- Use milestones to celebrate achievements
- Review milestone completion regularly"""
    },
    
    "project management": {
        "question": "What are the key principles of project management?",
        "answer": """Effective project management follows these key principles:
1. Clear objectives and scope
2. Strong leadership and team communication
3. Risk management and mitigation
4. Quality assurance throughout
5. Stakeholder engagement
6. Resource optimization
7. Continuous monitoring and control"""
    },
    
    "waterfall": {
        "question": "What is the Waterfall methodology?",
        "answer": """Waterfall is a linear, sequential project management methodology where each phase must be completed before the next begins. Phases typically include:
- Requirements
- Design
- Implementation
- Testing
- Deployment
- Maintenance

Best suited for projects with:
- Clear, fixed requirements
- Stable technology
- Well-understood scope
- Predictable outcomes"""
    }
}


def get_program_management_answer(topic: str) -> str:
    """
    Returns information about a program management topic.
    
    Args:
        topic: The topic to query (e.g., "gantt chart", "agile", "sprint", "critical path", "milestone")
    
    Returns:
        A detailed answer about the requested topic, or a message if topic not found
    """
    topic_lower = topic.lower().strip()
    
    # Handle variations and synonyms
    topic_mapping = {
        "gantt": "gantt chart",
        "gantt charts": "gantt chart",
        "chart": "gantt chart",
        "scrum": "sprint",  # Sprints are part of Scrum
        "sprints": "sprint",
        "agile methodology": "agile",
        "agile framework": "agile",
        "critical path method": "critical path",
        "cpm": "critical path",
        "milestones": "milestone",
        "project milestone": "milestone"
    }
    
    # Normalize the topic
    normalized_topic = topic_mapping.get(topic_lower, topic_lower)
    
    # Get the answer
    if normalized_topic in PROGRAM_MANAGEMENT_KB:
        kb_entry = PROGRAM_MANAGEMENT_KB[normalized_topic]
        return f"{kb_entry['question']}\n\n{kb_entry['answer']}"
    else:
        available_topics = ", ".join(PROGRAM_MANAGEMENT_KB.keys())
        return f"Sorry, I don't have information about '{topic}'. Available topics: {available_topics}"


# Example usage
if __name__ == "__main__":
    topics = ["gantt chart", "agile", "sprint", "critical path", "milestone"]
    
    print("Program Management Knowledge Base - Sample Responses\n")
    print("=" * 60)
    
    for topic in topics:
        print(f"\n{get_program_management_answer(topic)}")
        print("\n" + "-" * 60)

