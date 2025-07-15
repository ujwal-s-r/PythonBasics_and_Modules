# PythonREPLTool and general_tools 
import sys
from io import StringIO
from contextlib import redirect_stdout
from langchain_core.tools import tool

class PythonREPLTool:
    """A tool for executing python code"""
    name="python_repl"
    description="A tool for executing python code. Input should be a valid python code snippet."
    
    def __init__(self):
        self.globals = {}
        self.locals = {}
    
    def run(self, code: str) -> str:
        """Run the provided python code and return the output."""
        # Capture the output of the code execution
        old_stdout= sys.stdout
        redirect_output= StringIO()
        sys.stdout = redirect_output
        try:
            exec(code,self.globals,self.locals)
            output=redirect_output.getvalue()
        except Exception as e:
            output = f"Error: {str(e)}"
        finally:
            sys.stdout = old_stdout
        return output
python_repl_instance= PythonREPLTool()

@tool
def python_repl_tool(code: str) -> str:
    """Run the provided python code and return the output."""
    return python_repl_instance.run(code)
general_tools=[python_repl_tool] 


print("Python REPL Tool initialized successfully.")