
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.llm_config import shared_llm

def get_summarizer_chain():
    """
    Configures and returns the Summarizer Agent's chain.
    """
    summarizer_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a technical writer. Your task is to provide a concise summary and explanation of the provided Python code.
        Include:
        - The original high-level requirement.
        - A brief overview of the code's functionality.
        - How the code works (key functions/logic).
        - Any important notes about its usage or limitations.
        """),
        ("human", "Original Requirement: {overall_requirement}\n\n"
            "Final Generated Code:\n```python\n{final_code}\n```\n\n"
            "Development Process Notes: {process_notes}"), # Optional: pass phase details/review outcomes
    ])

    # The Summarizer Agent does not need tools
    summarizer_chain = summarizer_prompt | shared_llm | StrOutputParser()
    print("agents/summarize_agent.py: Summarizer Agent chain configured.")
    return summarizer_chain