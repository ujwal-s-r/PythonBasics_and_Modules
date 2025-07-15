from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from utils.llm_config import shared_llm
from utils.tools import general_tools

def get_review_agent_executor():
    """configures and returns the Review agent's AgentExecutor"""
    
    review_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a meticulous Code Reviewer. Your task is to identify bugs and errors in the provided Python code.
        You must execute the code using the `python_repl` tool to check for runtime errors.
        Focus ONLY on functional correctness, bugs, and errors. Do NOT provide stylistic suggestions, refactoring advice, or high-level improvements.
        If you find any bugs or errors, describe them clearly and concisely.
        If the code runs without errors and appears functionally correct based on the original requirement, respond ONLY with the word "NULL".
        """),
        ("human", "Overall Requirement: {overall_requirement}\n\n"
            "Code to Review:\n```python\n{code}\n```"),
        MessagesPlaceholder(variable_name="agent_scratchpad"), # For agent's internal thoughts
    ])
    review_agent=create_tool_calling_agent(
        llm=shared_llm,
        tools=general_tools,
        prompt=review_prompt,
        handle_parsing_errors=True,
    )
    review_agent_executor= AgentExecutor(
        agent=review_agent,
        tools=general_tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    print("agents/review_agent.py: Review agent executor configured successfully.")
    return review_agent_executor
    
    