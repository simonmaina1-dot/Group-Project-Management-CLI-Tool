"""
Authentication Service for the Library Management System.

This module handles user registration, login, and authentication.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from typing import Optional, Dict
from utils.file_handler import load_data, save_data
from models.user import User
from utils.validators import validate_username, validate_password, validate_role

# File paths
USER_FILE = "data/users.json"


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    
    Args:
        password: Plain text password
        
    Returns:
        Hexadecimal hash string
    """
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def register(username: str, password: str, role: str, email: str = "") -> Dict:
    """
    Register a new user and save to JSON file.
    
    Args:
        username: Unique username
        password: Plain text password (will be hashed)
        role: User role (admin/librarian/student)
        email: Optional email address
        
    Returns:
        Dictionary with success status and message
    """
    # Validate inputs
    valid, msg = validate_username(username)
    if not valid:
        return {'success': False, 'message': msg}
    
    valid, msg = validate_password(password)
    if not valid:
        return {'success': False, 'message': msg}
    
    valid, msg = validate_role(role)
    if not valid:
        return {'success': False, 'message': msg}
    
    # Load existing users
    users = load_data(USER_FILE)
    
    # Check if username already exists
    for user in users:
        if user.get('username') == username:
            return {'success': False, 'message': 'Username already exists'}
    
    # Create User object using the factory method
    user = User.create_user(username, password, role, email)
    
    # Add user to list
    users.append(user.to_dict())
    
    # Save updated list
    save_data(USER_FILE, users)
    
    return {'success': True, 'message': 'User registered successfully'}


def login(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user.
    
    Args:
        username: Username
        password: Plain text password
        
    Returns:
        User dictionary if successful, None otherwise
    """
    users = load_data(USER_FILE)
    hashed_password = hash_password(password)
    
    for user in users:
        if user.get('username') == username and user.get('password') == hashed_password:
            # Update last login
            user['last_login'] = datetime.now().isoformat()
            save_data(USER_FILE, users)
            return user
    
    return None


def get_user_by_username(username: str) -> Optional[Dict]:
    """
    Get user by username.
    
    Args:
        username: Username to search for
        
    Returns:
        User dictionary if found, None otherwise
    """
    users = load_data(USER_FILE)
    
    for user in users:
        if user.get('username') == username:
            return user
    
    return None


def update_user(username: str, updates: Dict) -> bool:
    """
    Update user information.
    
    Args:
        username: Username to update
        updates: Dictionary with fields to update
        
    Returns:
        True if successful, False otherwise
    """
    users = load_data(USER_FILE)
    
    for user in users:
        if user.get('username') == username:
            # Update allowed fields
            if 'email' in updates:
                user['email'] = updates['email']
            if 'role' in updates:
                user['role'] = updates['role']
            if 'is_active' in updates:
                user['is_active'] = updates['is_active']
            
            save_data(USER_FILE, users)
            return True
    
    return False


def delete_user(username: str) -> bool:
    """
    Delete a user.
    
    Args:
        username: Username to delete
        
    Returns:
        True if successful, False otherwise
    """
    users = load_data(USER_FILE)
    initial_count = len(users)
    
    # Find and remove user
    users = [user for user in users if user.get('username') != username]
    
    if len(users) < initial_count:  # Check if user was actually deleted
        save_data(USER_FILE, users)
        return True
    
    return False


def change_password(username: str, old_password: str, new_password: str) -> Dict:
    """
    Change user password.
    
    Args:
        username: Username
        old_password: Current password
        new_password: New password
        
    Returns:
        Dictionary with success status and message
    """
    # Verify old password
    users = load_data(USER_FILE)
    
    hashed_old = hash_password(old_password)
    
    for user in users:
        if user.get('username') == username and user.get('password') == hashed_old:
            # Validate new password
            valid, msg = validate_password(new_password)
            if not valid:
                return {'success': False, 'message': msg}
            
            # Update password
            user['password'] = hash_password(new_password)
            save_data(USER_FILE, users)
            return {'success': True, 'message': 'Password changed successfully'}
    
    return {'success': False, 'message': 'Invalid current password'}


def get_all_users() -> list:
    """
    Get all users.
    
    Returns:
        List of user dictionaries
    """
    return load_data(USER_FILE)

