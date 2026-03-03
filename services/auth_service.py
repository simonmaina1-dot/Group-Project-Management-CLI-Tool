"""
Authentication Service for the Library Management System.

This module handles user registration, login, and authentication
with session management for role-based access control.
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

# Session management - stores current logged in user
_current_session = None


# ==================== Password Hashing ====================

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


# ==================== Session Management ====================

def get_current_user() -> Optional[Dict]:
    """
    Get the currently logged in user.
    
    Returns:
        User dictionary if logged in, None otherwise
    """
    global _current_session
    return _current_session


def set_current_user(user: Optional[Dict]) -> None:
    """
    Set the current user session.
    
    Args:
        user: User dictionary or None to logout
    """
    global _current_session
    _current_session = user


def is_logged_in() -> bool:
    """
    Check if a user is currently logged in.
    
    Returns:
        True if logged in, False otherwise
    """
    return _current_session is not None


def get_current_user_role() -> Optional[str]:
    """
    Get the role of the current logged in user.
    
    Returns:
        Role string if logged in, None otherwise
    """
    if _current_session is None:
        return None
    return _current_session.get('role')


def is_admin() -> bool:
    """
    Check if current user is an admin.
    
    Returns:
        True if admin, False otherwise
    """
    return get_current_user_role() == 'admin'


def is_librarian() -> bool:
    """
    Check if current user is a librarian or admin.
    
    Returns:
        True if librarian or admin, False otherwise
    """
    role = get_current_user_role()
    return role in ['admin', 'librarian']


def is_student() -> bool:
    """
    Check if current user is a student.
    
    Returns:
        True if student, False otherwise
    """
    return get_current_user_role() == 'student'


def check_access(required_roles: list) -> tuple:
    """
    Check if current user has access based on their role.
    
    Args:
        required_roles: List of roles that are allowed
        
    Returns:
        Tuple of (has_access: bool, message: str)
    """
    if not is_logged_in():
        return False, "Please login to access this feature."
    
    user_role = get_current_user_role()
    if user_role not in required_roles:
        return False, f"Access denied. Required roles: {', '.join(required_roles)}. Your role: {user_role}"
    
    return True, ""


# ==================== User Registration ====================

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


# ==================== User Login ====================

def login(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user and start a session.
    
    Args:
        username: Username
        password: Plain text password
        
    Returns:
        User dictionary if successful, None otherwise
    """
    global _current_session
    
    users = load_data(USER_FILE)
    hashed_password = hash_password(password)
    
    for user in users:
        if user.get('username') == username and user.get('password') == hashed_password:
            # Check if account is active
            if not user.get('is_active', True):
                return None
            
            # Update last login
            user['last_login'] = datetime.now().isoformat()
            save_data(USER_FILE, users)
            
            # Set current session
            _current_session = user
            return user
    
    return None


def logout() -> None:
    """
    Logout the current user and clear the session.
    """
    global _current_session
    _current_session = None


# ==================== User Management ====================

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


# ==================== User Role Management (Admin only) ====================

def update_user_role(username: str, new_role: str, current_user: Optional[Dict]) -> Dict:
    """
    Update a user's role. Only admins can change roles.
    
    Args:
        username: Username to update
        new_role: New role to assign
        current_user: The admin performing the action
        
    Returns:
        Dictionary with success status and message
    """
    # Check if current user is admin
    if current_user is None:
        return {'success': False, 'message': 'Please login first.'}
    
    if current_user.get('role') != 'admin':
        return {'success': False, 'message': 'Only admins can change user roles.'}
    
    # Validate role
    valid, msg = validate_role(new_role)
    if not valid:
        return {'success': False, 'message': msg}
    
    # Update user role
    users = load_data(USER_FILE)
    
    for user in users:
        if user.get('username') == username:
            old_role = user.get('role', 'unknown')
            user['role'] = new_role
            save_data(USER_FILE, users)
            return {'success': True, 'message': f"Role changed from '{old_role}' to '{new_role}' for user '{username}'."}
    
    return {'success': False, 'message': f"User '{username}' not found."}


def deactivate_user(username: str, current_user: Optional[Dict]) -> Dict:
    """
    Deactivate a user account. Only admins can do this.
    
    Args:
        username: Username to deactivate
        current_user: The admin performing the action
        
    Returns:
        Dictionary with success status and message
    """
    if current_user is None:
        return {'success': False, 'message': 'Please login first.'}
    
    if current_user.get('role') != 'admin':
        return {'success': False, 'message': 'Only admins can deactivate users.'}
    
    users = load_data(USER_FILE)
    
    for user in users:
        if user.get('username') == username:
            if not user.get('is_active', True):
                return {'success': False, 'message': 'User is already deactivated.'}
            
            user['is_active'] = False
            save_data(USER_FILE, users)
            return {'success': True, 'message': f"User '{username}' has been deactivated."}
    
    return {'success': False, 'message': f"User '{username}' not found."}


def activate_user(username: str, current_user: Optional[Dict]) -> Dict:
    """
    Activate a user account. Only admins can do this.
    
    Args:
        username: Username to activate
        current_user: The admin performing the action
        
    Returns:
        Dictionary with success status and message
    """
    if current_user is None:
        return {'success': False, 'message': 'Please login first.'}
    
    if current_user.get('role') != 'admin':
        return {'success': False, 'message': 'Only admins can activate users.'}
    
    users = load_data(USER_FILE)
    
    for user in users:
        if user.get('username') == username:
            if user.get('is_active', True):
                return {'success': False, 'message': 'User is already active.'}
            
            user['is_active'] = True
            save_data(USER_FILE, users)
            return {'success': True, 'message': f"User '{username}' has been activated."}
    
    return {'success': False, 'message': f"User '{username}' not found."}

