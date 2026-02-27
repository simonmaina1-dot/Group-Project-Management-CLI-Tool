"""
File Handler Module - Handles reading and writing JSON files.

This module provides simple functions to save and load data
from JSON files in the data folder.
"""

import json
import os


def read_json(filename):
    """
    Read data from a JSON file.
    
    Args:
        filename: Name of the file to read (e.g., 'users.json')
        
    Returns:
        A list of data (empty list if file doesn't exist)
    """
    # Check if file exists
    if not os.path.exists(filename):
        return []
    
    try:
        # Open and read the JSON file
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except:
        # Return empty list if there's any error
        return []


def write_json(filename, data):
    """
    Write data to a JSON file.
    
    Args:
        filename: Name of the file to write to
        data: List of data to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open and write to the JSON file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False


def append_item(filename, item):
    """
    Add a new item to the JSON file.
    
    Args:
        filename: Name of the file
        item: Dictionary to add
        
    Returns:
        True if successful
    """
    # Read existing data
    data = read_json(filename)
    
    # Add new item to the list
    data.append(item)
    
    # Save the updated list
    return write_json(filename, data)


def update_item(filename, item_id, updates):
    """
    Update an existing item in the JSON file.
    
    Args:
        filename: Name of the file
        item_id: ID of the item to update
        updates: Dictionary with the changes
        
    Returns:
        True if updated, False if not found
    """
    # Read existing data
    data = read_json(filename)
    
    # Find and update the item
    for item in data:
        if item.get('id') == item_id:
            item.update(updates)
            return write_json(filename, data)
    
    return False


def delete_item(filename, item_id):
    """
    Delete an item from the JSON file.
    
    Args:
        filename: Name of the file
        item_id: ID of the item to delete
        
    Returns:
        True if deleted, False if not found
    """
    # Read existing data
    data = read_json(filename)
    
    # Count items before
    old_count = len(data)
    
    # Keep only items that don't match the ID
    data = [item for item in data if item.get('id') != item_id]
    
    # Check if something was deleted
    if len(data) < old_count:
        return write_json(filename, data)
    
    return False


def find_by_id(filename, item_id):
    """
    Find a single item by its ID.
    
    Args:
        filename: Name of the file
        item_id: ID to search for
        
    Returns:
        The item if found, None otherwise
    """
    # Read existing data
    data = read_json(filename)
    
    # Search for the item
    for item in data:
        if item.get('id') == item_id:
            return item
    
    return None


def find_all(filename):
    """
    Get all items from a JSON file.
    
    Args:
        filename: Name of the file
        
    Returns:
        List of all items
    """
    return read_json(filename)

