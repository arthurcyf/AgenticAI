import os  # Provides path resolution, directory creation, and file-existence checks
from google.genai import types  # Type definitions for declaring the Gemini function schema

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(os.path.join(working_directory))  # Resolve the sandbox root to an absolute path
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))  # Resolve the target file path relative to the sandbox root
    if not abs_file_path.startswith(abs_working_directory):  # Path escape check: reject writes outside the sandbox
        return f'Error: "{file_path}" is not in the working directory'  # Return error string so the agent loop can continue
    
    parent_dir = os.path.dirname(abs_file_path)  # Get the directory that must exist before the file can be created
    if not os.path.exists(parent_dir):  # Only attempt to create directories if they are missing
        try:
            os.makedirs(parent_dir, exist_ok=True)  # Create all missing parent directories in one call
        except Exception as e:
            return f"Error creating directories:{parent_dir} = {e}"  # Return error string so the agent loop can continue
    try:
        with open(abs_file_path, "w") as f:  # Open (or create) the file in write mode, overwriting existing content
            f.write(content)  # Write the model-generated content to the file
        return f'Successfully wrote to "{file_path}"'  # Confirm success so the model can observe it
    
    except Exception as e:
        return f"Error writing to file: {e}"  # Return exception as a string so the agent loop can continue rather than crash
    
# Schema that tells the Gemini model the name, description, and parameters of this tool
schema_write_file = types.FunctionDeclaration(
    name="write_file",  # The exact name the model must use when requesting this tool
    description="Writes content to a specified file relative to the working directory, creating any necessary directories",  # Helps the model decide when to use this tool
    parameters=types.Schema(
        type=types.Type.OBJECT,  # Parameters are passed as a JSON object
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,  # The file_path argument must be a string
                description="Path to the file to write content to, relative to the working directory",  # Guides the model on how to populate this argument
            ),
            "content": types.Schema(
                type=types.Type.STRING,  # The content argument must be a string
                description="The content to write to the file",  # Guides the model on how to populate this argument
            ),
        },
    ),
)