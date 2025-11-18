import os

def get_files_info(working_directory, directory="."):
    # treat directory as relative path within the working _directory
    full_path = os.path.join(working_directory, directory)

    full_path = os.path.abspath(full_path)
    working_directory = os.path.abspath(working_directory)

    # Security check: ensure full_path is within working_directory
    if not full_path.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Check if directory exists
    if not os.path.exists(full_path):
        return f'Error: Directory "{directory}" does not exist'
    
    # Check if it's actually a directory
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        items = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            items.append(f" - {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(items)
    
    except Exception as e:
        return f"Error: {str(e)}"
    