import os
from config import MAX_CHAR
from google.genai import types

def get_file_content(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)
    full_path = os.path.abspath(full_path)

    working_directory = os.path.abspath(working_directory)

    # ensure file_path isn't outside working directory
    if not full_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # check if the path is a file
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, 'r') as f:
            file_contents = f.read(MAX_CHAR + 1)

            if len(file_contents) > MAX_CHAR:
                truncated_content = file_contents[:MAX_CHAR]
                return f'{truncated_content}\n[...File "{full_path}" truncated at {MAX_CHAR} characters]'
            
            return file_contents
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file constrained to the working directory. Returns the file content as a string, with automatic truncation for large files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory. Can include subdirectories (e.g., 'pkg/calculator.py', 'main.py'). Must be a valid file path within the working directory boundaries.",
            ),
        },
    ),
)