from google.genai import types  # Import types for constructing structured tool-response messages
from functions.get_files_info import get_files_info  # Tool: lists files and directories
from functions.get_file_content import get_file_content  # Tool: reads the content of a file
from functions.write_file import write_file  # Tool: writes content to a file
from functions.run_python_file import run_python_file  # Tool: executes a Python file and captures output

working_directory = "calculator"  # The sandbox root — all tool file operations are restricted to this directory

def call_function(function_call_part, verbose=False):
    if verbose:  # In verbose mode, print full argument details for debugging
        print(f"Function Call: {function_call_part.name} with arguments {function_call_part.args}")
    else:  # In normal mode, print a compact one-line summary
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        
    result = ""  # Will hold the tool's string output; stays empty if no tool name matched
        
    if function_call_part.name == "get_files_info":  # Model requested a directory listing
        result = get_files_info(working_directory=working_directory, directory=function_call_part.args.get("directory"))  # Inject the sandbox root; model only supplies the subdirectory
    elif function_call_part.name == "get_file_content":  # Model requested the contents of a file
        file_path = function_call_part.args.get("file_path")  # Extract the relative file path from the model's arguments
        result = get_file_content(working_directory=working_directory, file_path=file_path)  # Read the file within the sandbox
    elif function_call_part.name == "write_file":  # Model requested writing content to a file
        file_path = function_call_part.args.get("file_path")  # Extract the target path from the model's arguments
        content = function_call_part.args.get("content")  # Extract the content string to write
        result = write_file(working_directory=working_directory, file_path=file_path, content=content)  # Write the file within the sandbox
    elif function_call_part.name == "run_python_file":  # Model requested executing a Python script
        file_path = function_call_part.args.get("file_path")  # Extract the script path from the model's arguments
        args = function_call_part.args.get("args", [])  # Extract optional CLI arguments; default to empty list if not provided
        result = run_python_file(working_directory=working_directory, file_path=file_path, args=args)  # Run the script within the sandbox
    if result == "":  # If result is still empty, no tool name matched — the model called an unknown function
        return types.Content(
            role="tool",  # Mark this message as coming from the tool layer
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,  # Echo the unknown function name back
                    response={"error": f"Unknown function: {function_call_part.name}"},  # Return an error payload so the model can observe and recover
                )
            ],
        )
    return types.Content(
        role="tool",  # Mark this message as coming from the tool layer
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,  # Echo the called function name so the model can correlate the response
                response={"result": result},  # Wrap the tool output so the model can observe it in the next iteration
            )
        ],
    )