import os
from google.genai import types

def write_file(working_directory, file_path, content):

    full_path = os.path.join(working_directory, file_path)
    full_path = os.path.abspath(full_path)
    working_directory = os.path.abspath(working_directory)

    # ensure file_path is within working directory
    if not full_path.startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        parent_dir = os.path.dirname(full_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
            
        with open(full_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Create or overwrite a file with specified content within the working directory. Automatically creates parent directories if they don't exist. Returns success message with character count or error details.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path where the file should be created or overwritten, relative to the working directory. Can include subdirectories that will be created automatically (e.g., 'config.txt', 'data/output.json', 'src/utils/helper.py').",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file. This will completely replace any existing file content. Can be empty string to create an empty file.",
            ),
        },
        required=["file_path", "content"]
    ),
)
