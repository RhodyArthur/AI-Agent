# AI Code Assistant

An intelligent CLI tool that uses Google's Gemini API to autonomously perform coding tasks by executing predefined functions in a secure sandbox environment.

## Purpose

This AI agent helps developers by automating common coding tasks such as:

- Analyzing codebases and file structures
- Reading and writing files
- Running Python scripts and tests
- Debugging and fixing code issues
- Generating documentation and code

The agent operates within a secure working directory boundary, preventing it from accessing or modifying files outside the designated project folder.

## How It Works

1. **Task Input**: You provide a natural language description of what you want to accomplish
2. **Function Planning**: The AI analyzes your request and creates a plan using available functions
3. **Execution Loop**: The agent executes functions iteratively (up to 20 iterations):
   - Lists files and directories
   - Reads file contents
   - Writes or modifies files
   - Executes Python scripts
4. **Results**: The agent provides a final response with the completed task or error details

## Available Functions

- **`get_files_info`**: Lists files and directories with sizes and types
- **`get_file_content`**: Reads file contents (with automatic truncation for large files)
- **`write_file`**: Creates or overwrites files with specified content
- **`run_python_file`**: Executes Python scripts with optional arguments and captures output

## Installation

1. Clone this repository:

```bash
git clone https://github.com/RhodyArthur/AI-Agent.git
cd AI-Agent
```

2. Install dependencies:

```bash
uv install
```

3. Set up your Gemini API key:

```bash
# Create a .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## Usage

### Basic Usage

```bash
uv run main.py "your task description here"
```

### Verbose Mode (shows detailed function calls and token usage)

```bash
uv run main.py "your task description here" --verbose
```

### Example Commands

**Analyze project structure:**

```bash
uv run main.py "what files are in the root directory?"
```

**Read file contents:**

```bash
uv run main.py "show me the contents of main.py"
```

**Run tests:**

```bash
uv run main.py "run the calculator tests"
```

**Create or modify files:**

```bash
uv run main.py "create a README file with project documentation"
```

**Debug code issues:**

```bash
uv run main.py "find and fix any syntax errors in the calculator"
```

## Security Features

- **Sandboxed Execution**: All file operations are restricted to the `./calculator` working directory
- **Path Validation**: Prevents directory traversal attacks and unauthorized file access
- **Timeout Protection**: Python script execution is limited to 30 seconds
- **Input Sanitization**: All inputs are validated before function execution

## Project Structure

```
ai-agent/
├── main.py              # Main CLI interface and conversation loop
├── call_function.py     # Function dispatcher and execution handler
├── config.py           # Configuration settings (MAX_CHAR limit)
├── prompts.py          # System prompts for the AI agent
├── functions/          # Individual function implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/         # Example project (working directory)
└── tests.py           # Function testing utilities
```

## Requirements

- Python 3.8+
- Google Gemini API access
- `google-genai` library
- `python-dotenv` library

## Error Handling

The agent includes robust error handling for:

- API rate limits (429 errors)
- File permission issues
- Invalid file paths
- Execution timeouts
- Network connectivity issues
