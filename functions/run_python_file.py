import os  # Provides path resolution and file-existence checks
import subprocess  # Allows launching the Python interpreter as a child process
from google.genai import types  # Type definitions for declaring the Gemini function schema

def run_python_file(working_directory, file_path, args = []):
    abs_working_directory = os.path.abspath(os.path.join(working_directory))  # Resolve the sandbox root to an absolute path
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))  # Resolve the target script path relative to the sandbox root
    if not abs_file_path.startswith(abs_working_directory):  # Path escape check: reject execution of files outside the sandbox
        return f'Error: "{file_path}" is not in the working directory'  # Return error string so the agent loop can continue
    
    if not os.path.isfile(abs_file_path):  # Ensure the path points to an actual file before attempting to run it
        return f'Error: "{file_path}" is not a file path'  # Return error string so the agent loop can continue
    
    if not file_path.endswith(".py"):  # Restrict execution to Python files only
        return f'Error: "{file_path}" is not a Python file'  # Prevents accidentally running non-Python files
    
    try:
        final_args = ["python3", abs_file_path] + args  # Build the command: python3 interpreter + script path + any extra arguments
        result = subprocess.run(final_args, cwd=abs_working_directory, timeout=30, capture_output=True, text=True)  # Run the script with a 30-second timeout, capturing stdout and stderr as text
        final_string = f"""STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"""  # Combine both output streams into one readable string for the model
        
        if result.stdout == "" and result.stderr == "":  # Script ran but produced no output at all
            final_string = "Python file ran successfully but produced no output."  # Replace empty output with a descriptive message
        if result.returncode != 0:  # Non-zero exit code means the script encountered an error
            final_string = f"Error: Python file exited with return code {result.returncode}\n\n" + final_string  # Prepend the error code so the model knows execution failed
        return final_string  # Return the combined output to the caller
    
    except Exception as e:
        return f"Error running file: {e}"  # Return exception as a string so the agent loop can continue rather than crash

# Schema that tells the Gemini model the name, description, and parameters of this tool
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",  # The exact name the model must use when requesting this tool
    description="Runs a specified Python file relative to the working directory",  # Helps the model decide when to use this tool
    parameters=types.Schema(
        type=types.Type.OBJECT,  # Parameters are passed as a JSON object
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,  # The file_path argument must be a string
                description="Path to the Python file to run, relative to the working directory",  # Guides the model on how to populate this argument
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,  # args is a list of values
                description="Optional arguments to pass to the Python file",  # Guides the model that this argument is optional
                items=types.Schema(type=types.Type.STRING)  # Each item in the list must be a string
            )
        },
    ),
)