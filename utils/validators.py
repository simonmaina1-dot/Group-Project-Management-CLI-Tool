"""Validators for the CLI Library Management System."""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    # Allow digits, spaces, dashes, and parentheses
    pattern = r'^[\d\s\-\(\)]+$'
    return bool(re.match(pattern, phone)) and len(phone) >= 10


def validate_isbn(isbn: str) -> bool:
    """
    Validate ISBN format (10 or 13 digits).
    
    Args:
        isbn: ISBN to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    # Remove hyphens and spaces
    isbn = isbn.replace('-', '').replace(' ', '')
    
    # Check for 10 or 13 digits
    if len(isbn) == 10:
        return isbn[:9].isdigit() and (isbn[9].isdigit() or isbn[9] == 'X')
    elif len(isbn) == 13:
        return isbn.isdigit()
    return False


def validate_username(username: str) -> bool:
    """
    Validate username format.
    
    Args:
        username: Username to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    # Username should be 3-20 characters, alphanumeric and underscores
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(pattern, username))


def validate_password(password: str) -> bool:
    """
    Validate password strength.
    
    Args:
        password: Password to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    # Password should be at least 6 characters
    return len(password) >= 6


def validate_role(role: str) -> bool:
    """
    Validate user role.
    
    Args:
        role: Role to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    valid_roles = ['admin', 'librarian', 'member']
    return role.lower() in valid_roles


def validate_positive_integer(value: any) -> bool:
    """
    Validate positive integer.
    
    Args:
        value: Value to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    try:
        num = int(value)
        return num > 0
    except (ValueError, TypeError):
        return False


def validate_year(year: any) -> bool:
    """
    Validate publication year.
    
    Args:
        year: Year to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    try:
        year_int = int(year)
        # Reasonable range for book publication
        return 1000 <= year_int <= 2100
    except (ValueError, TypeError):
        return False


def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input by removing extra whitespace.
    
    Args:
        input_str: Input string to sanitize.
        
    Returns:
        Sanitized string.
    """
    return input_str.strip()

