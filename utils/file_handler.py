import json
import os

def load_data(file_path):
    """load data from a JSON file.
    return a list of data, or an empty list if the file doesn't exist."""
    if not os.path.exists(file_path):
        # Create the data directory if it doesn't exist
        data_dir = os.path.dirname(file_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return []
    with open(file_path, "r") as file:
        data = json.load(file)
        # Return list if data is a list, otherwise wrap in list or return empty list
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data] if data else []
        return []

def save_data(file_path, data):
    """save data to a JSON file."""
    # Ensure directory exists
    data_dir = os.path.dirname(file_path)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

