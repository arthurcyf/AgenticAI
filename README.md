# AI Agent

An AI coding agent powered by Google's Gemini API that can interact with your filesystem and execute Python code through function calling.

## Features

- **File Operations**: List directories, read file contents, write to files
- **Code Execution**: Run Python files and capture their output
- **AI-Powered**: Uses Gemini 2.5 Flash with function calling
- **Safe Sandboxing**: All file operations are relative to the working directory

## Prerequisites

- Python 3.13 or higher
- Google Gemini API key

## Setup

1. **Install dependencies**

	Using `uv` (recommended):
	```bash
	uv sync
	```

	Or using `pip`:
	```bash
	pip install -r requirements.txt
	```

2. **Configure API key**

	Create a `.env` file in the project root:
	```bash
	GEMINI_API_KEY=your_api_key_here
	```

	Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Usage

### Basic Usage

```bash
uv run main.py "your prompt here"
```

Or with Python directly:
```bash
python main.py "your prompt here"
```

### Verbose Mode

Enable detailed output with the `--verbose` flag:

```bash
uv run main.py "your prompt here" --verbose
```

This will display:
- The user prompt
- Prompt token count
- Response token count

### Example Prompts

```bash
# List files in the calculator directory
uv run main.py "List all files in the calculator directory"

# Read a file
uv run main.py "Read the contents of calculator/pkg/calculator.py"

# Create a new file
uv run main.py "Create a file called hello.py that prints 'Hello, World!'"

# Run a Python script
uv run main.py "Run the calculator/main.py file with input '3 + 7 * 2'"

# Complex coding task
uv run main.py "Create a simple web scraper that fetches the title of a webpage"
```

## Project Structure

```
aiagent/
├── main.py                 # Main agent loop
├── call_function.py        # Function call handler
├── config.py              # Configuration (MAX_CHARS limit)
├── pyproject.toml         # Project dependencies
├── functions/             # Function schemas and implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/            # Example application
│   ├── main.py
│   └── pkg/
│       └── calculator.py
└── tests.py              # Tests

```

## Available Functions

The AI agent has access to the following functions:

1. **get_files_info**: List files and directories in a specified path
2. **get_file_content**: Read the contents of a file (with character limit)
3. **write_file**: Write content to a file (creates directories as needed)
4. **run_python_file**: Execute a Python file and capture its output

## Configuration

- **MAX_CHARS**: Maximum characters to read from a file (default: 10,000)
- **max_iters**: Maximum iterations for the agent loop (default: 20)

## How It Works

1. User provides a prompt via command line
2. Prompt is sent to Gemini with available function schemas
3. Gemini decides which functions to call (if any)
4. Functions are executed locally and results are sent back
5. Process repeats until Gemini provides a final response

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
