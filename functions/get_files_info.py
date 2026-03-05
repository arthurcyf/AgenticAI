import os  # Provides path resolution and directory listing utilities
from google.genai import types  # Type definitions for declaring the Gemini function schema
# Example output this tool produces:
# - README.md: file_size=1032 bytes, is_dir=False
# - src: file_size=128 bytes, is_dir=True
# - package.json: file_size=1234 bytes, is_dir=False

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(os.path.join(working_directory))  # Resolve the sandbox root to an absolute path
    abs_directory = " "  # Placeholder; will be set in the branches below
    if directory is None:  # No subdirectory specified — default to listing the sandbox root itself
        abs_directory = os.path.abspath(working_directory)  # Use the working directory as the listing target
    else:
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))  # Resolve the requested subdirectory relative to the sandbox root
    if not abs_directory.startswith(abs_working_directory):  # Path escape check: reject anything outside the sandbox
        return f'Error: "{directory}" is not a directory'  # Return error string so the agent loop can continue
    
    final_response = ""  # Accumulates one formatted line per directory entry
    contents = os.listdir(abs_directory)  # List all entries (files and folders) in the target directory
    for content in contents:  # Iterate over each entry
        is_dir = os.path.isdir(os.path.join(abs_directory, content))  # True if this entry is a subdirectory
        file_size = os.path.getsize(os.path.join(abs_directory, content))  # Size in bytes
        final_response += f"- {content}: file_size={file_size} bytes, is_dir={is_dir}\n"  # Append a formatted summary line
    return final_response  # Return the full listing string to the caller


# Schema that tells the Gemini model the name, description, and parameters of this tool
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",  # The exact name the model must use when requesting this tool
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",  # Helps the model decide when to use this tool
    parameters=types.Schema(
        type=types.Type.OBJECT,  # Parameters are passed as a JSON object
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,  # The directory argument must be a string
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",  # Guides the model on how to populate this argument
            ),
        },
    ),
)