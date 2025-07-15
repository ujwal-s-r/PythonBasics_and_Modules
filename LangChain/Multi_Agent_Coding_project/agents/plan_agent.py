from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.llm_config import shared_llm

def get_plan_agent_chain():
    """configure the plan agent chain and returns the chain"""
    plant_prompt = ChatPromptTemplate.from_messages(
        [
            ("system","""you are a expert software architect, your task is to break down users high level coding requirements
            into structured, phase by phase deevelopment plan. The plan MUST consist of 1 to 3 distinct phases. Each phases
            should be clearly described with its objectives.
            Respond in a clear, concise JSON array format, where each element is an object with 'phase_number' (integer) and 'description' (string).
        Example:
        [
        {"phase_number": 1, "description": "Setup project, define main function, handle basic input parsing."},
        {"phase_number": 2, "description": "Implement core logic for feature X."},
        {"phase_number": 3, "description": "Add error handling and edge case management."}
        ]"""),
        ("human", "Requirement: {requirement}"),
        ]
    )
    plan_generation_chain= plant_prompt | shared_llm | StrOutputParser()
    print("agents/plan_agent.py: Plan Agent Chain configured successfully.")
    return plan_generation_chain