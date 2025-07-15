import json
from agents.plan_agent import get_plan_agent_chain
from agents.code_agent import _get_coding_agent_executor
from agents.summarize_agent import get_summarizer_chain
from agents.review_agent import get_review_agent_executor

print("main_pipeline.py: Starting Multi-Agent Coding Project Pipeline...")

plan_agent_chain = get_plan_agent_chain()
coding_agent_executor = _get_coding_agent_executor()
summarizer_chain = get_summarizer_chain()
review_agent_executor = get_review_agent_executor()

print("main_pipeline.py: All agents configured successfully.")

def run_code_development_project(user_requirement: str,max_coding_retries_per_phase:int=2):
    """Orchestractes the multi agent code development projects
    Args:
        user_requirement (str): The high-level requirement for the project.
        max_coding_retries_per_phase (int): Maximum retries for coding agent per phase.
    """
    print("startd.....")
    print("user requirements:", user_requirement)
    
    print("Manager agent requesting plan")
    development_plan=[]
    try:
        plan_raw=plan_agent_chain.invoke({"requirement": user_requirement})
        development_plan = json.loads(plan_raw["plan"])
        print("Manager agent received plan:")
        for phase in development_plan:
            print(f"phase number{phase['phase_number']}: {phase['description']}")
    except json.JSONDecodeError as e:
        print(f"Error parsing plan JSON: {e}")
        return
    except Exception as e:
        print(f"Manager: An unexpected error occurred during planning: {e}")
        print("Manager: Aborting project due to planning error.")
        return
    accumulated_code = []
    processed_notes = []
    
    for i, phase in enumerate(development_plan):
        phase_number = phase['phase_number']
        phase_description = phase['description']
        print(f"Manager: Starting Phase {phase_number} - {phase_description}")
        current_phase_code = ""
        feedback_to_coder=""
        retries=0
        
        while retries< max_coding_retries_per_phase:
            try:
                coding_input={
                    "overall_requirements": user_requirement,
                    "phase_description": phase_description,
                    "feedback":feedback_to_coder,
                    "previous_code": "\n".join(accumulated_code) if accumulated_code else "",
                }
                generated_code= coding_agent_executor.invoke(coding_input)['output']
                print(f"Manager: Phase {phase_number} code generated successfully.")
                
                print("Manager: Sending code for the reciew for phase ", phase_number)
                review_input={
                    "overall_requirement": user_requirement,
                    "code": generated_code,
                    "phase_objectives": phase_description,
                }
                review_result=review_agent_executor.invoke(review_input)['output']
                
                if review_result=="NULL":
                    print(f"Manager: Phase {phase_number} code review passed.")
                    current_phase_code = generated_code
                    accumulated_code.append(current_phase_code)
                    processed_notes.append(f"Phase {phase_number} completed successfully.")
                    break
                else:
                    print(f"Manager: Review feedback for Phase {phase_number} found issue")
                    feedback_to_coder = review_result
                    retries += 1
                    processed_notes.append(f"Phase {phase_number}- {phase_description}")
                    
            except Exception as e:
                print(f"Manager: Error during coding phase {phase_number}: {e}")
                retries += 1
                processed_notes.append(f"Phase {phase_number} encountered an error: {e}")
        if retries> max_coding_retries_per_phase:
            print(f"Manager: Phase {phase_number} failed after {max_coding_retries_per_phase} retries. Aborting project.")
            return
    print("Manager: Generating summary phase")
    final_code_string="\n\n".join(accumulated_code)
    final_process_notes="\n".join(processed_notes)
    
    summarizer_input={
        "overall_requirement": user_requirement,
        "final_code": final_code_string,
        "process_notes": final_process_notes,
    }
    try:
        final_summary = summarizer_chain.invoke(summarizer_input)
        print("\n--- Final Project Summary ---")
        print(final_summary)
        print("\n--- Final Generated Code ---")
        print(final_code_string)
    except Exception as e:
        print(f"Manager: Error during summarization: {e}")
        print("Manager: Project completed with errors during summarization. Final code (if any) below:")
        print(final_code_string)

    print("\n--- Project Finished ---")

if __name__== "__main__":
    user_requirement = input("Enter the high-level project requirement: ")
    run_code_development_project(user_requirement)