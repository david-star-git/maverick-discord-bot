import json
from imports import console

# Helper function to load JSON data
def load_json(file_path: str):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        console.warning(f"File not found: {file_path}")
    except json.JSONDecodeError:
        console.error(f"Invalid JSON format: {file_path}")
    return {}