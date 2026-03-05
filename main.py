import os  # Provides functions for interacting with the operating system (env vars, paths)
import sys  # Provides access to command-line arguments (sys.argv) and process control (sys.exit)
from dotenv import load_dotenv  # Loads key=value pairs from a .env file into environment variables
from google import genai  # Google Generative AI client library used to communicate with Gemini
from google.genai import types  # Type definitions (Content, Part, Tool, Schema) for structuring Gemini API calls
from functions.get_files_info import schema_get_files_info  # Gemini function schema that describes the get_files_info tool
from functions.get_file_content import schema_get_file_content  # Gemini function schema that describes the get_file_content tool
from functions.write_file import schema_write_file  # Gemini function schema that describes the write_file tool
from functions.run_python_file import schema_run_python_file  # Gemini function schema that describes the run_python_file tool
from call_function import call_function  # Dispatcher that receives model function-call requests and routes them to implementations

def main():

    load_dotenv()  # Read the .env file and inject its values (e.g. GEMINI_API_KEY) into os.environ
    api_key = os.getenv("GEMINI_API_KEY")  # Retrieve the API key from environment variables
    client = genai.Client(api_key=api_key)  # Create an authenticated Gemini API client
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file content (with a maximum character limit to prevent excessive output)
    - Write content to a file (creating any necessary directories)
    - Run a Python file and capture its output
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """  # System instruction that sets the agent's role and lists the tools it can use

    if len(sys.argv) < 2:  # sys.argv[0] is the script name, so fewer than 2 args means no prompt was given
        print("Usage: python main.py <prompt>")  # Print usage hint so the user knows how to run the script
        sys.exit(1)  # Exit with a non-zero code to signal incorrect usage
    verbose_flag = False  # Default to non-verbose; only token counts and raw calls are printed when True
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":  # Check if the optional --verbose flag was passed as the third argument
        verbose_flag = True  # Enable verbose output (prompt text + token counts per iteration)
    prompt = sys.argv[1]  # The user's natural-language task passed as the first CLI argument
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),  # Seed the conversation history with the user's prompt
    ]
    
    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],  # Register all tool schemas so the model knows what functions are available and how to call them
    )
    
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt  # Attach tool definitions and the system prompt to every model request
    )
    
    max_iters = 20  # Safety cap on the agent loop to prevent infinite reasoning cycles
    for i in range(max_iters):  # Reason-act-observe loop: each iteration is one model call
        response = client.models.generate_content(  # Send the full conversation history to Gemini and get the next response
            model="gemini-2.5-flash",  # Use Gemini 2.5 Flash (fast, cost-efficient model)
            contents=messages,  # Pass the accumulated conversation so the model has full context
            config=config  # Apply tool schemas and system instruction
        )
        
        if response is None:  # Guard against a null response from the API
            print("Error: No response received.")  # Inform the user there was no response
            return  # Exit early — nothing to process
        
        if verbose_flag:  # Only print debug info when --verbose was passed
            print(f"User Prompt: {prompt}")  # Echo the original user prompt
            print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")  # Show how many tokens the prompt consumed
            print(f"Response Tokens: {response.usage_metadata.candidates_token_count}")  # Show how many tokens the response used

        if response.candidates:  # Check that the model returned at least one candidate response
            for candidate in response.candidates:  # Iterate over each candidate (usually just one)
                if candidate is None or candidate.content is None:  # Skip malformed candidates with missing content
                    print("Error: Candidate or candidate content is None.")  # Warn about the bad candidate
                    continue  # Move on to the next candidate
                messages.append(candidate.content)  # Append the model's response to the conversation history for the next iteration
        
        if response.function_calls:  # Check if the model wants to call one or more tools
            for function_call_part in response.function_calls:  # Iterate over each requested function call
                result = call_function(function_call_part, verbose=verbose_flag)  # Execute the tool and capture its output
                messages.append(result)  # Append the tool result to the conversation so the model can observe it in the next iteration
        else:
            print(response.text)  # No more tool calls — the model produced a final answer, print it and end the loop
        
main()  # Entry point: run the agent when this script is executed directly
# print(get_files_info("calculator"))