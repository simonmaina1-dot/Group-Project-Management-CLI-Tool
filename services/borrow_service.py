"""
Borrow Service for the Library Management System.

This module handles all borrow record operations with role-based access control.
- Admin: Full access to all borrow operations
- Librarian: Can extend due dates, view all borrow records
- Student: Can only view their own borrow records
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from utils.file_handler import load_data, save_data
from models.borrow_record import BorrowRecord

# File paths
BOOK_FILE = "data/books.json"
BORROW_FILE = "data/borrow_records.json"


# ==================== Access Control Helpers ====================

def check_borrow_access(current_user: Optional[Dict], action: str) -> tuple:
    """
    Check if current user has permission to perform the borrow action.
    
    Args:
        current_user: The logged in user dictionary or None
        action: The action being performed ('view_all', 'extend', 'view_own')
        
    Returns:
        Tuple: bool, message: str)
    """
    if current_user is None:
        return False, "Please login to access borrow records."
    
    role = current_user.get('role', '')
    
    if action in ['view_all', 'extend']:
        # Only admin and librarian can view all records or extend
        if role not in ['admin', 'librarian']:
            return False, f"Access denied. Only admins and librarians can {action.replace('_', ' ')}."
    
    return True, ""


# ==================== Borrow Record Operations ====================

def get_all_borrow_records(current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Get all borrow records. Admin and librarians only.
    
    Args:
        current_user: The logged in user (must be admin or librarian)
        
    Returns:
        List of borrow record dictionaries
    """
    # Check access
    has_access, msg = check_borrow_access(current_user, 'view_all')
    if not has_access:
        return []
    
    records = load_data(BORROW_FILE)
    if not isinstance(records, list):
        return []
    return records


def get_user_borrow_records(username: str, current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Get borrow records for a specific user.
    - Admin/Librarian: Can view any user's records
    - Student: Can only view their own records
    
    Args:
        username: Username to get records for
        current_user: The logged in user
        
    Returns:
        List of borrow record dictionaries
    """
    # Check if logged in
    if current_user is None:
        return []
    
    role = current_user.get('role', '')
    
    # Students can only view their own records
    if role == 'student':
        if username != current_user.get('username'):
            return []
    
    records = load_data(BORROW_FILE)
    if not isinstance(records, list):
        return []
    
    return [record for record in records if record.get('user_name') == username]


def get_active_borrow_records(current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Get all active (not returned) borrow records. Admin and librarians only.
    
    Args:
        current_user: The logged in user (must be admin or librarian)
        
    Returns:
        List of active borrow record dictionaries
    """
    # Check access
    has_access, msg = check_borrow_access(current_user, 'view_all')
    if not has_access:
        return []
    
    records = load_data(BORROW_FILE)
    if not isinstance(records, list):
        return []
    
    return [record for record in records if record.get('status') == 'active']


def get_overdue_records(current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Get all overdue borrow records. Admin and librarians only.
    
    Args:
        current_user: The logged in user (must be admin or librarian)
        
    Returns:
        List of overdue borrow record dictionaries
    """
    # Check access
    has_access, msg = check_borrow_access(current_user, 'view_all')
    if not has_access:
        return []
    
    records = load_data(BORROW_FILE)
    if not isinstance(records, list):
        return []
    
    now = datetime.now()
    overdue = []
    for record in records:
        if record.get('status') == 'active':
            return_date_str = record.get('return_date')
            if return_date_str:
                return_date = datetime.fromisoformat(return_date_str)
                if now > return_date:
                    overdue.append(record)
    
    return overdue


def extend_borrow_record(username: str, isbn: str, days: int, current_user: Optional[Dict] = None) -> Dict:
    """
    Extend the due date of a borrow record. Admin and librarians only.
    
    Args:
        username: Username of the borrower
        isbn: ISBN of the book
        days: Number of days to extend
        current_user: The logged in user (must be admin or librarian)
        
    Returns:
        Dictionary with success status and message
    """
    # Check access
    has_access, msg = check_borrow_access(current_user, 'extend')
    if not has_access:
        return {'success': False, 'message': msg}
    
    # Validate days
    if days < 1 or days > 30:
        return {'success': False, 'message': 'Extension must be between 1 and 30 days.'}
    
    # Find and update the borrow record
    records = load_data(BORROW_FILE)
    
    for record in records:
        if record.get('user_name') == username and record.get('isbn') == isbn:
            if record.get('status') != 'active':
                return {'success': False, 'message': 'This book has already been returned.'}
            
            # Extend the return date
            return_date_str = record.get('return_date')
            if return_date_str:
                current_return_date = datetime.fromisoformat(return_date_str)
                new_return_date = current_return_date + timedelta(days=days)
                record['return_date'] = new_return_date.isoformat()
                record['is_renewed'] = True
                record['renewal_count'] = record.get('renewal_count', 0) + 1
                record['last_renewal'] = datetime.now().isoformat()
                
                save_data(BORROW_FILE, records)
                
                # Also update the book record
                books = load_data(BOOK_FILE)
                for book in books:
                    if book.get('isbn') == isbn:
                        borrowed_by = book.get('borrowed_by', [])
                        for br in borrowed_by:
                            if br.get('user') == username:
                                br['due_date'] = new_return_date.isoformat()
                                br['is_renewed'] = True
                                br['renewal_count'] = record['renewal_count']
                                break
                        save_data(BOOK_FILE, books)
                
                return {'success': True, 'message': f'Borrow extended by {days} days. New due date: {new_return_date.strftime("%Y-%m-%d")}'}
    
    return {'success': False, 'message': 'Borrow record not found.'}


def get_borrow_statistics(current_user: Optional[Dict] = None) -> Dict:
    """
    Get borrowing statistics. Admin and librarians only.
    
    Args:
        current_user: The logged in user (must be admin or librarian)
        
    Returns:
        Dictionary with statistics
    """
    # Check access
    has_access, msg = check_borrow_access(current_user, 'view_all')
    if not has_access:
        return {'success': False, 'message': msg}
    
    records = load_data(BORROW_FILE)
    if not isinstance(records, list):
        records = []
    
    now = datetime.now()
    total_records = len(records)
    active_records = sum(1 for r in records if r.get('status') == 'active')
    returned_records = total_records - active_records
    
    overdue_count = 0
    for record in records:
        if record.get('status') == 'active':
            return_date_str = record.get('return_date')
            if return_date_str:
                return_date = datetime.fromisoformat(return_date_str)
                if now > return_date:
                    overdue_count += 1
    
    # Count by role
    users = {}
    for record in records:
        username = record.get('user_name')
        if username:
            users[username] = users.get(username, 0) + 1
    
    return {
        'success': True,
        'statistics': {
            'total_borrows': total_records,
            'active_borrows': active_records,
            'returned_borrows': returned_records,
            'overdue_borrows': overdue_count,
            'unique_borrowers': len(users)
        }
    }


def mark_book_lost(isbn: str, current_user: Optional[Dict] = None) -> Dict:
    """
    Mark a borrowed book as lost. Admin and librarians only.
    
    Args:
        isbn: ISBN of the book
        current_user: The logged in user (must be admin or librarian)
        
    Returns:
        Dictionary with success status and message
    """
    # Check access
    has_access, msg = check_borrow_access(current_user, 'extend')
    if not has_access:
        return {'success': False, 'message': msg}
    
    books = load_data(BOOK_FILE)
    
    for book in books:
        if book.get('isbn') == isbn:
            book['is_lost'] = True
            book['lost_at'] = datetime.now().isoformat()
            book['lost_by'] = current_user.get('username') if current_user else 'system'
            
            # Reduce available copies
            book['available_copies'] = max(0, book.get('available_copies', 1) - 1)
            
            save_data(BOOK_FILE, books)
            return {'success': True, 'message': f'Book {isbn} marked as lost.'}
    
    return {'success': False, 'message': 'Book not found.'}


def get_user_borrow_history(username: str, current_user: Optional[Dict] = None) -> List[Dict]:
    """
    Get complete borrow history for a user.
    
    Args:
        username: Username to get history for
        current_user: The logged in user
        
    Returns:
        List of borrow record dictionaries
    """
    # Students can only view their own history
    if current_user is None:
        return []
    
    role = current_user.get('role', '')
    if role == 'student' and username != current_user.get('username'):
        return []
    
    records = load_data(BORROW_FILE)
    if not isinstance(records, list):
        return []
    
    return [record for record in records if record.get('user_name') == username]

