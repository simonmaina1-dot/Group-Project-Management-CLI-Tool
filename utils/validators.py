"""Validators for the CLI Library Management System.

This module provides validation functions for various data types used throughout
the library management system, including emails, phone numbers, ISBNs, usernames,
passwords, roles, and other common fields.
"""

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
    # Email pattern breakdown:
    # [a-zA-Z0-9._%+-]+ = local part (letters, numbers, dots, underscores, percent, plus, hyphen)
    # @ = literal @ symbol
    # [a-zA-Z0-9.-]+ = domain name (letters, numbers, dots, hyphens)
    # \. = literal dot
    # [a-zA-Z]{2,}$ = top-level domain (at least 2 letters)
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
    # This pattern accommodates various phone number formats (e.g., +1-234-567-8900, (234) 567-8900)
    pattern = r'^[\d\s\-\(\)]+$'
    # Ensure phone number has at least 10 digits to be valid
    return bool(re.match(pattern, phone)) and len(phone) >= 10


def validate_isbn(isbn: str) -> bool:
    """
    Validate ISBN format (10 or 13 digits).
    
    Args:
        isbn: ISBN to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    # Remove hyphens and spaces to get clean ISBN
    isbn = isbn.replace('-', '').replace(' ', '')
    
    # Check for 10 or 13 digits
    if len(isbn) == 10:
        # First 9 characters must be digits, 10th can be digit or 'X' (representing 10)
        return isbn[:9].isdigit() and (isbn[9].isdigit() or isbn[9] == 'X')
    elif len(isbn) == 13:
        # All 13 characters must be digits
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
    # Username rules:
    # ^ = start of string
    # [a-zA-Z0-9_]{3,20} = 3 to 20 characters, alphanumeric and underscores only
    # $ = end of string
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

