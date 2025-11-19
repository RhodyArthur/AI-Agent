import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    full_path = os.path.abspath(full_path)
    working_directory = os.path.abspath(working_directory)

    if not full_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = ['python', full_path] + args
        
        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Format output according to requirements
        output_parts = []
        
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")
        
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")
        
        # Check for non-zero exit code
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        # Return formatted output or "No output produced."
        if output_parts:
            return "\n".join(output_parts)
        else:
            return "No output produced."
        
    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path}" timed out after 30 seconds'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file within the working directory with optional command-line arguments. Captures stdout, stderr, and exit codes with a 30-second timeout to prevent infinite execution.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory. Must be a .py file within the working directory boundaries (e.g., 'main.py', 'tests.py', 'pkg/calculator.py').",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python script. Each argument should be a string (e.g., ['arg1', 'arg2', '--flag']). Defaults to empty list if not provided."
            )
        },
        required=["file_path"]
    ),
)