# Interview Notes: Agentic AI Concepts in This Project

This file breaks down the ML/agentic concepts implemented in this codebase so you can explain the project clearly in interviews.

## 1) What You Built (30-second summary)

I built a lightweight coding agent using Gemini function calling. The model receives a user prompt, chooses from a fixed set of tools (file listing, file reading/writing, Python execution), observes tool outputs, and iterates until it reaches a final answer.

## 2) Core Agent Pattern

This project follows a ReAct-style loop:

1. **Reason** about the user prompt
2. **Act** by calling a tool
3. **Observe** tool output
4. Repeat until completion

In the code, this is the iterative loop in `main.py` (`max_iters = 20`) with model responses and tool responses appended to shared `messages` state.

## 3) Why Function Calling Matters

Instead of letting the model generate arbitrary shell commands, the action space is constrained to typed tools via Gemini `FunctionDeclaration` schemas.

Benefits:
- Better reliability and determinism
- Clear API contract between model and runtime
- Easier to debug and audit

## 4) Tool-Orchestration Layer

`call_function.py` acts as the runtime router:
- Receives model-emitted function calls
- Dispatches to Python implementations in `functions/`
- Returns structured tool responses back to the model

This separation is important in production systems: planning (LLM) and execution (runtime) are decoupled.

## 5) Safety / Guardrails Implemented

Even in a small project, you implemented practical safety boundaries:

- **Path sandboxing**: tools verify paths stay inside a configured working directory
- **Output control**: file reads are capped by `MAX_CHARS` to prevent context overload
- **Execution limits**: Python execution uses timeout (`30s`) and captures stdout/stderr

These are foundational patterns for secure, tool-using agents.

## 6) State Management in Agent Systems

The `messages` list stores:
- user messages
- model responses
- tool outputs

This persistent context enables multi-step reasoning across tool calls and is key to agent behavior beyond one-shot prompting.

## 7) Key Trade-offs You Can Discuss

Strengths of current design:
- Simple and transparent architecture
- Easy to reason about and extend
- Good educational baseline for agent systems

What you would add for production:
- Better error taxonomy and retries
- Structured logging/telemetry and tracing
- Permissioning and stricter sandboxing
- Tool result validation and fallback strategies

## 8) Potential Interview Questions + Good Answers

### Q: “How is this different from a normal chatbot?”
A: A normal chatbot mostly returns text. This system can decide actions, call tools, observe outputs, and iteratively solve tasks.

### Q: “What makes this an agent?”
A: It has an action loop with tool use and stateful multi-step reasoning, not just single-turn response generation.

### Q: “What reliability mechanisms did you add?”
A: Constrained function schemas, bounded iteration count, path checks, read truncation, and execution timeout.

### Q: “How would you improve it?”
A: Add tracing, retries, richer error handling, stronger sandboxing, and evaluation harnesses for tool-calling success rate.

## 9) Elevator Pitch (10–15 seconds)

I implemented a minimal tool-using AI agent on Gemini. It uses structured function calling, a ReAct-style loop, and basic safety guardrails to perform real filesystem and code-execution tasks in multiple steps.

## 10) Additional Notes You Asked For

### What is a schema and what is its purpose?

A schema is a structured contract that defines:
- the function name,
- expected parameters,
- parameter types,
- and descriptions of how each field should be used.

In this project, each tool exposes a Gemini `FunctionDeclaration` schema. Its purpose is to make tool calling reliable: the model knows exactly what actions are available and how to format arguments, while the runtime gets predictable inputs.

### What is the sequence of function calls when a prompt is typed into the CLI?

High-level sequence:

1. You run: `uv run main.py "<prompt>"`
2. `main.py` loads env vars, creates Gemini client, and prepares message/tool config.
3. `client.models.generate_content(...)` is called with:
	- current `messages`,
	- tool schemas,
	- system instruction.
4. If the model returns `function_calls`, `main.py` sends each to `call_function(...)`.
5. `call_function.py` dispatches to the matching tool implementation:
	- `get_files_info(...)`, or
	- `get_file_content(...)`, or
	- `write_file(...)`, or
	- `run_python_file(...)`.
6. Tool output is wrapped as a tool response (`types.Part.from_function_response`) and appended to `messages`.
7. The loop calls Gemini again with updated context.
8. When the model stops requesting tools, final text is printed to CLI.

This is the full reason-act-observe loop.

### Why are strings used instead of raising errors?

In this implementation, tools return error strings (for example `Error: ...`) instead of raising exceptions so the agent loop can keep running and the model can reason over failures as normal observations.

Why this helps in a minimal agent:
- avoids crashing the full loop on recoverable tool issues,
- keeps tool outputs serializable and easy to pass back to the model,
- gives the model a chance to self-correct (try another file/path/action).

Trade-off:
- less strict than typed exceptions,
- harder to categorize errors programmatically.

For production, a stronger pattern is returning structured error objects (error code + message + metadata), while still avoiding uncontrolled crashes.

## 11) Purpose of Each Tool in This Project

### `get_files_info`

Purpose:
- Gives the agent visibility into the workspace structure.
- Helps the model decide *what file to inspect next* before reading/writing.

Why it matters:
- Prevents blind guesses about file names and paths.
- Supports planning-style behavior (explore first, then act).

### `get_file_content`

Purpose:
- Retrieves file content so the model can reason over existing code.
- Enables tasks like summarization, debugging, and code edits.

Why it matters:
- Provides grounded context from real files.
- Includes truncation control (`MAX_CHARS`) to limit prompt growth.

### `write_file`

Purpose:
- Persists the model’s generated output to disk.
- Creates parent directories automatically when needed.

Why it matters:
- Converts model decisions into real artifacts (code/config/docs).
- Enables end-to-end automation instead of text-only suggestions.

### `run_python_file`

Purpose:
- Executes Python scripts and returns stdout/stderr to the model.
- Allows the agent to validate whether generated code actually runs.

Why it matters:
- Creates an execution feedback loop (generate → run → fix).
- Supports iterative debugging and self-correction.

## 12) Further Improvements to Scale Up the Agent

### A) Structured error model and retries

- Replace plain error strings with typed payloads (`code`, `message`, `retriable`, `metadata`).
- Add retry policies with exponential backoff for transient failures.

### B) Better planning and task decomposition

- Introduce an explicit planner step for multi-file tasks.
- Track subgoals/checkpoints so long tasks are more reliable.

### C) Memory and retrieval

- Add short-term memory summarization to avoid context bloat.
- Add retrieval over project files (embeddings/index) for larger repos.

### D) Tooling expansion

- Add tools for search, lint, tests, formatting, and dependency inspection.
- Add language-agnostic execution tools (not only Python) for broader use.

### E) Security and isolation

- Move code execution into stronger isolation (container/sandbox).
- Add allowlists for paths and commands, and redact sensitive outputs.

### F) Observability and evaluation

- Add tracing for each model/tool turn (latency, failures, token usage).
- Build an eval suite for task success rate, tool-call accuracy, and regression testing.

### G) Human-in-the-loop controls

- Require approval gates before destructive actions (delete/overwrite).
- Provide diff previews before writing files.

### H) Multi-agent or specialized roles (advanced)

- Split responsibilities across planner, coder, and reviewer agents.
- Use a verifier agent to check correctness before final output.
