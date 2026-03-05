import os  # Provides path resolution and file-existence checks
from google.genai import types  # Type definitions for declaring the Gemini function schema
from config import MAX_CHARS as MAX_CHARACTER_LIMIT  # Character cap to prevent large files from filling the model's context window

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(os.path.join(working_directory))  # Resolve the sandbox root to an absolute path
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))  # Resolve the requested file path relative to the sandbox root
    if not abs_file_path.startswith(abs_working_directory):  # Path escape check: reject anything outside the sandbox
        return f'Error: "{file_path}" is not in the working directory'  # Return error string so the agent loop can continue
    
    if not os.path.isfile(abs_file_path):  # Ensure the path points to a file, not a directory or non-existent path
        return f'Error: "{file_path}" is not a file path'  # Return error string so the agent loop can continue
    
    file_content_string = ""  # Will hold the file's text content
    try:
        with open(abs_file_path, "r") as f:  # Open the file in read mode
            file_content_string = f.read(MAX_CHARACTER_LIMIT)  # Read up to the character cap to avoid context overflow
            if len(file_content_string) == MAX_CHARACTER_LIMIT:  # If we hit the cap exactly, the file was likely truncated
                file_content_string += "\n\n[Truncated: File content exceeds maximum character limit]"  # Append a notice so the model knows the output was cut off
        return file_content_string  # Return the (possibly truncated) file content
    
    except Exception as e:
        return f"Error reading file: {e}"  # Return exception as a string so the agent loop can continue rather than crash
    
# Schema that tells the Gemini model the name, description, and parameters of this tool
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",  # The exact name the model must use when requesting this tool
    description="Gets the content of a specified file relative to the working directory, with a maximum character limit to prevent excessive output",  # Helps the model decide when to use this tool
    parameters=types.Schema(
        type=types.Type.OBJECT,  # Parameters are passed as a JSON object
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,  # The file_path argument must be a string
                description="Path to the file to retrieve content from, relative to the working directory",  # Guides the model on how to populate this argument
            ),
        },
    ),
)