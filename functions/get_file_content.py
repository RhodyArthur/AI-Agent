import os
from config import MAX_CHAR

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



