from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from utils.llm_config import shared_llm
from utils.tools import general_tools

def _get_coding_agent_executor():
    """"configures and returns Coding agent AgentExecutor"""
    
    coding_prompt= ChatPromptTemplate.from_messages([
        ("system", """You are a Python developer. Your task is to write Python code for a specific phase of a larger project.
        You will be given the overall project requirement and the current phase's objectives.
        Focus ONLY on the code for the CURRENT phase. Do not write code for future phases.
        If you are fixing bugs, incorporate the feedback provided.
        Respond ONLY with the Python code. Do not include any explanations or extra text.
        ```python
        # Your code here
        ```
        """),
        ("human", "Overall Requirement: {overall_requirement}\n\n"
            "Current Phase Objectives: {phase_objectives}\n\n"
            "{feedback}"), # This placeholder will be filled by the Manager if there's review feedback
        MessagesPlaceholder(variable_name="agent_scratchpad"), # For agent's internal thoughts/tool use
    ])
    
    coding_agent=create_tool_calling_agent(
        llm=shared_llm,
        tools=general_tools,
        prompt=coding_prompt,
        handle_parsing_errors=True,
    )
    
    coding_agent_executor = AgentExecutor(
        agent=coding_agent,
        tools=general_tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    
    print("agents/code_agents.py: Coding agent executor configured successfully.")
    return coding_agent_executor

        