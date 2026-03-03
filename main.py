#!/usr/bin/env python3
"""
Library Management System - CLI Entry Point

A simple Python CLI application for managing a library system.
Features:
- User registration and login
- Role-based access control (Admin, Librarian, Student)
- Book management (Admin only)
- Borrow/Return operations
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import (
    register, login, logout, get_current_user, is_logged_in,
    get_current_user_role, is_admin, is_librarian
)
from services.book_service import (
    add_book, list_books, list_available_books, delete_book, search_book,
    borrow_book, return_book, get_borrowed_books, get_overdue_books
)
from services.borrow_service import (
    get_all_borrow_records, get_user_borrow_records, extend_borrow_record,
    get_borrow_statistics, get_overdue_records
)


# ==================== Helper Functions ====================

def print_success(message):
    """Print success message."""
    print(f"SUCCESS: {message}")


def print_error(message):
    """Print error message."""
    print(f"ERROR: {message}")


def print_info(message):
    """Print info message."""
    print(f"INFO: {message}")


def print_warning(message):
    """Print warning message."""
    print(f"WARNING: {message}")


def get_current_user():
    """Get the current logged in user."""
    from services.auth_service import get_current_user as auth_get_current_user
    return auth_get_current_user()


def display_books(books, title="Book List"):
    """Display books in a table format."""
    if not books:
        print_info("No books found.")
        return
    
    # Define column widths
    col_no = 4
    col_title = 35
    col_author = 25
    col_isbn = 15
    col_available = 10
    
    # Print title
    print(f"\n{title}")
    print("=" * (col_no + col_title + col_author + col_isbn + col_available + 8))
    
    # Print header
    print(f"{'#':<{col_no}} | {'Title':<{col_title}} | {'Author':<{col_author}} | {'ISBN':<{col_isbn}} | {'Available':<{col_available}}")
    print("-" * (col_no + col_title + col_author + col_isbn + col_available + 8))
    
    # Print each book row
    for idx, book in enumerate(books, 1):
        title = book.get('title', 'N/A')[:col_title-1]
        author = book.get('author', 'N/A')[:col_author-1]
        isbn = book.get('isbn', 'N/A')[:col_isbn-1]
        available = book.get('available_copies', 0)
        
        print(f"{idx:<{col_no}} | {title:<{col_title}} | {author:<{col_author}} | {isbn:<{col_isbn}} | {available:<{col_available}}")
    
    # Print footer
    print("=" * (col_no + col_title + col_author + col_isbn + col_available + 8))
    print(f"Total books: {len(books)}")


def display_users(users, title="User List"):
    """Display users in a table format."""
    if not users:
        print_info("No users found.")
        return
    
    col_no = 4
    col_username = 20
    col_role = 12
    col_email = 25
    col_status = 10
    
    print(f"\n{title}")
    print("=" * (col_no + col_username + col_role + col_email + col_status + 8))
    
    print(f"{'#':<{col_no}} | {'Username':<{col_username}} | {'Role':<{col_role}} | {'Email':<{col_email}} | {'Status':<{col_status}}")
    print("-" * (col_no + col_username + col_role + col_email + col_status + 8))
    
    for idx, user in enumerate(users, 1):
        username = user.get('username', 'N/A')[:col_username-1]
        role = user.get('role', 'N/A')[:col_role-1]
        email = user.get('email', 'N/A')[:col_email-1]
        status = 'Active' if user.get('is_active', True) else 'Inactive'
        
        print(f"{idx:<{col_no}} | {username:<{col_username}} | {role:<{col_role}} | {email:<{col_email}} | {status:<{col_status}}")
    
    print("=" * (col_no + col_username + col_role + col_email + col_status + 8))
    print(f"Total users: {len(users)}")


def display_borrow_records(records, title="Borrow Records"):
    """Display borrow records in a table format."""
    if not records:
        print_info("No records found.")
        return
    
    col_book = 30
    col_user = 15
    col_borrow = 12
    col_due = 12
    col_status = 10
    
    print(f"\n{title}")
    print("=" * (col_book + col_user + col_borrow + col_due + col_status + 8))
    
    print(f"{'Book Title':<{col_book}} | {'User':<{col_user}} | {'Borrowed':<{col_borrow}} | {'Due Date':<{col_due}} | {'Status':<{col_status}}")
    print("-" * (col_book + col_user + col_borrow + col_due + col_status + 8))
    
    for record in records:
        book_title = record.get('book_title', 'N/A')[:col_book-1]
        username = record.get('user_name', 'N/A')[:col_user-1]
        borrow_date = record.get('borrow_date', 'N/A')[:col_borrow-1]
        due_date = record.get('return_date', 'N/A')[:col_due-1]
        status = record.get('status', 'N/A')[:col_status-1]
        
        print(f"{book_title:<{col_book}} | {username:<{col_user}} | {borrow_date:<{col_borrow}} | {due_date:<{col_due}} | {status:<{col_status}}")
    
    print("=" * (col_book + col_user + col_borrow + col_due + col_status + 8))
    print(f"Total records: {len(records)}")


# ==================== Command Handlers ====================

def handle_register(args):
    """Handle user registration."""
    result = register(args.username, args.password, args.role)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_login(args):
    """Handle user login."""
    user = login(args.username, args.password)
    if user:
        print_success(f"Welcome, {user['username']} ({user['role']})")
    else:
        print_error("Invalid username or password.")


def handle_logout(args):
    """Handle user logout."""
    logout()
    print_success("Logged out successfully.")


def handle_add_book(args):
    """Handle adding a book (Admin only)."""
    current_user = get_current_user()
    
    # Check if admin
    if current_user is None:
        print_error("Please login first.")
        return
    
    if current_user.get('role') != 'admin':
        print_error("Access denied. Only admins can add books.")
        return
    
    result = add_book(args.title, args.author, args.isbn, args.copies, current_user)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_list_books(args):
    """Handle listing books (All logged in users)."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    books = list_books(current_user)
    display_books(books, "All Books in Library")


def handle_delete_book(args):
    """Handle deleting a book (Admin only)."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    if current_user.get('role') != 'admin':
        print_error("Access denied. Only admins can delete books.")
        return
    
    result = delete_book(args.isbn, current_user)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_search_book(args):
    """Handle searching for a book (All logged in users)."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    books = search_book(args.query, current_user)
    if books:
        display_books(books, f"Search Results for '{args.query}'")
    else:
        print_info(f"No books found matching '{args.query}'")


def handle_borrow_book(args):
    """Handle borrowing a book."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    # For students, they can only borrow for themselves
    username = args.username
    if current_user.get('role') == 'student':
        username = current_user.get('username')
    
    result = borrow_book(username, args.isbn, current_user)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_return_book(args):
    """Handle returning a book."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    # For students, they can only return their own books
    username = args.username
    if current_user.get('role') == 'student':
        username = current_user.get('username')
    
    result = return_book(username, args.isbn, current_user)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_my_borrows(args):
    """Handle viewing user's own borrowed books."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    username = current_user.get('username')
    books = get_borrowed_books(username, current_user)
    display_books(books, f"Books Borrowed by {username}")


def handle_all_borrows(args):
    """Handle viewing all borrow records (Admin/Librarian only)."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    if current_user.get('role') not in ['admin', 'librarian']:
        print_error("Access denied. Only admins and librarians can view all borrow records.")
        return
    
    records = get_all_borrow_records(current_user)
    display_borrow_records(records, "All Borrow Records")


def handle_overdue(args):
    """Handle viewing overdue books (Admin/Librarian only)."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    if current_user.get('role') not in ['admin', 'librarian']:
        print_error("Access denied. Only admins and librarians can view overdue books.")
        return
    
    records = get_overdue_records(current_user)
    display_borrow_records(records, "Overdue Borrow Records")


def handle_extend_borrow(args):
    """Handle extending borrow due date (Admin/Librarian only)."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    if current_user.get('role') not in ['admin', 'librarian']:
        print_error("Access denied. Only admins and librarians can extend borrow periods.")
        return
    
    try:
        days = int(args.days) if hasattr(args, 'days') else 7
    except ValueError:
        days = 7
    
    result = extend_borrow_record(args.username, args.isbn, days, current_user)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_borrow_stats(args):
    """Handle viewing borrow statistics (Admin/Librarian only)."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    if current_user.get('role') not in ['admin', 'librarian']:
        print_error("Access denied. Only admins and librarians can view statistics.")
        return
    
    result = get_borrow_statistics(current_user)
    if result.get('success'):
        stats = result.get('statistics', {})
        print("\n" + "="*40)
        print("Borrow Statistics")
        print("="*40)
        print(f"Total Borrows: {stats.get('total_borrows', 0)}")
        print(f"Active Borrows: {stats.get('active_borrows', 0)}")
        print(f"Returned Borrows: {stats.get('returned_borrows', 0)}")
        print(f"Overdue Borrows: {stats.get('overdue_borrows', 0)}")
        print(f"Unique Borrowers: {stats.get('unique_borrowers', 0)}")
        print("="*40)
    else:
        print_error(result.get('message'))


def handle_view_all_users(args):
    """Handle viewing all users (Admin only)."""
    from services.auth_service import get_all_users
    
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    if current_user.get('role') != 'admin':
        print_error("Access denied. Only admins can view all users.")
        return
    
    users = get_all_users()
    # Remove password from display
    for user in users:
        user.pop('password', None)
    display_users(users, "All Users")


def handle_available_books(args):
    """Handle viewing available books."""
    current_user = get_current_user()
    
    if current_user is None:
        print_error("Please login first.")
        return
    
    books = list_available_books(current_user)
    display_books(books, "Available Books in Library")


# ==================== Interactive Mode ====================

def interactive_mode():
    """Run the CLI in interactive menu mode."""
    
    while True:
        current_user = get_current_user()
        
        print("\n" + "="*50)
        print("Library Management System")
        print("="*50)
        
        if current_user:
            role = current_user.get('role', 'Unknown')
            print(f"Logged in as: {current_user['username']} ({role})")
        else:
            print("Not logged in")
        
        print("-"*50)
        
        # Show menu based on login status and role
        menu_options = []
        
        if not current_user:
            menu_options = [
                ("1", "Register"),
                ("2", "Login"),
                ("3", "Exit")
            ]
        else:
            role = current_user.get('role')
            
            if role == 'admin':
                menu_options = [
                    ("1", "Add Book"),
                    ("2", "List All Books"),
                    ("3", "List Available Books"),
                    ("4", "Search Book"),
                    ("5", "Delete Book"),
                    ("6", "Borrow Book"),
                    ("7", "Return Book"),
                    ("8", "My Borrowed Books"),
                    ("9", "All Borrow Records"),
                    ("10", "Overdue Books"),
                    ("11", "Extend Borrow"),
                    ("12", "View Statistics"),
                    ("13", "View All Users"),
                    ("14", "Logout"),
                    ("15", "Exit")
                ]
            elif role == 'librarian':
                menu_options = [
                    ("1", "List All Books"),
                    ("2", "List Available Books"),
                    ("3", "Search Book"),
                    ("4", "Borrow Book"),
                    ("5", "Return Book"),
                    ("6", "My Borrowed Books"),
                    ("7", "All Borrow Records"),
                    ("8", "Overdue Books"),
                    ("9", "Extend Borrow"),
                    ("10", "View Statistics"),
                    ("11", "Logout"),
                    ("12", "Exit")
                ]
            else:  # student
                menu_options = [
                    ("1", "List Available Books"),
                    ("2", "Search Book"),
                    ("3", "Borrow Book"),
                    ("4", "Return Book"),
                    ("5", "My Borrowed Books"),
                    ("6", "Logout"),
                    ("7", "Exit")
                ]
        
        for key, label in menu_options:
            print(f"{key}. {label}")
        
        print("-"*50)
        
        choice = input("Enter your choice: ").strip()
        
        # Handle based on role
        if not current_user:
            # Not logged in
            if choice == "1":
                # Register
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                role = input("Enter role (admin/librarian/student): ").strip().lower()
                handle_register(type('obj', (object,), {'username': username, 'password': password, 'role': role})())
            
            elif choice == "2":
                # Login
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                handle_login(type('obj', (object,), {'username': username, 'password': password})())
            
            elif choice == "3":
                print_info("Exiting system... Thank you for using the library system.")
                break
            
            else:
                print_error("Invalid choice. Please try again.")
        
        else:
            role = current_user.get('role')
            
            if role == 'admin':
                _handle_admin_menu(choice, current_user)
            elif role == 'librarian':
                _handle_librarian_menu(choice, current_user)
            else:  # student
                _handle_student_menu(choice, current_user)


def _handle_admin_menu(choice, current_user):
    """Handle admin menu choices."""
    
    if choice == "1":
        # Add Book
        title = input("Enter book title: ").strip()
        author = input("Enter author: ").strip()
        isbn = input("Enter ISBN: ").strip()
        copies = input("Enter number of copies: ").strip()
        try:
            copies = int(copies)
            handle_add_book(type('obj', (object,), {'title': title, 'author': author, 'isbn': isbn, 'copies': copies})())
        except ValueError:
            print_error("Invalid number of copies.")
    
    elif choice == "2":
        # List All Books
        handle_list_books(type('obj', (object,), {})())
    
    elif choice == "3":
        # List Available Books
        handle_available_books(type('obj', (object,), {})())
    
    elif choice == "4":
        # Search Book
        query = input("Enter book title or author to search: ").strip()
        handle_search_book(type('obj', (object,), {'query': query})())
    
    elif choice == "5":
        # Delete Book
        isbn = input("Enter ISBN to delete: ").strip()
        handle_delete_book(type('obj', (object,), {'isbn': isbn})())
    
    elif choice == "6":
        # Borrow Book
        isbn = input("Enter ISBN to borrow: ").strip()
        username = input("Enter username (or press Enter for self): ").strip()
        if not username:
            username = current_user['username']
        handle_borrow_book(type('obj', (object,), {'username': username, 'isbn': isbn})())
    
    elif choice == "7":
        # Return Book
        isbn = input("Enter ISBN to return: ").strip()
        username = input("Enter username (or press Enter for self): ").strip()
        if not username:
            username = current_user['username']
        handle_return_book(type('obj', (object,), {'username': username, 'isbn': isbn})())
    
    elif choice == "8":
        # My Borrowed Books
        handle_my_borrows(type('obj', (object,), {})())
    
    elif choice == "9":
        # All Borrow Records
        handle_all_borrows(type('obj', (object,), {})())
    
    elif choice == "10":
        # Overdue Books
        handle_overdue(type('obj', (object,), {})())
    
    elif choice == "11":
        # Extend Borrow
        username = input("Enter username: ").strip()
        isbn = input("Enter ISBN: ").strip()
        days = input("Enter number of days to extend (default 7): ").strip()
        handle_extend_borrow(type('obj', (object,), {'username': username, 'isbn': isbn, 'days': days})())
    
    elif choice == "12":
        # View Statistics
        handle_borrow_stats(type('obj', (object,), {})())
    
    elif choice == "13":
        # View All Users
        handle_view_all_users(type('obj', (object,), {})())
    
    elif choice == "14":
        # Logout
        handle_logout(type('obj', (object,), {})())
    
    elif choice == "15":
        print_info("Exiting system... Thank you for using the library system.")
        sys.exit(0)
    
    else:
        print_error("Invalid choice. Please try again.")


def _handle_librarian_menu(choice, current_user):
    """Handle librarian menu choices."""
    
    if choice == "1":
        # List All Books
        handle_list_books(type('obj', (object,), {})())
    
    elif choice == "2":
        # List Available Books
        handle_available_books(type('obj', (object,), {})())
    
    elif choice == "3":
        # Search Book
        query = input("Enter book title or author to search: ").strip()
        handle_search_book(type('obj', (object,), {'query': query})())
    
    elif choice == "4":
        # Borrow Book
        isbn = input("Enter ISBN to borrow: ").strip()
        username = input("Enter username (or press Enter for self): ").strip()
        if not username:
            username = current_user['username']
        handle_borrow_book(type('obj', (object,), {'username': username, 'isbn': isbn})())
    
    elif choice == "5":
        # Return Book
        isbn = input("Enter ISBN to return: ").strip()
        username = input("Enter username (or press Enter for self): ").strip()
        if not username:
            username = current_user['username']
        handle_return_book(type('obj', (object,), {'username': username, 'isbn': isbn})())
    
    elif choice == "6":
        # My Borrowed Books
        handle_my_borrows(type('obj', (object,), {})())
    
    elif choice == "7":
        # All Borrow Records
        handle_all_borrows(type('obj', (object,), {})())
    
    elif choice == "8":
        # Overdue Books
        handle_overdue(type('obj', (object,), {})())
    
    elif choice == "9":
        # Extend Borrow
        username = input("Enter username: ").strip()
        isbn = input("Enter ISBN: ").strip()
        days = input("Enter number of days to extend (default 7): ").strip()
        handle_extend_borrow(type('obj', (object,), {'username': username, 'isbn': isbn, 'days': days})())
    
    elif choice == "10":
        # View Statistics
        handle_borrow_stats(type('obj', (object,), {})())
    
    elif choice == "11":
        # Logout
        handle_logout(type('obj', (object,), {})())
    
    elif choice == "12":
        print_info("Exiting system... Thank you for using the library system.")
        sys.exit(0)
    
    else:
        print_error("Invalid choice. Please try again.")


def _handle_student_menu(choice, current_user):
    """Handle student menu choices."""
    
    if choice == "1":
        # List Available Books
        handle_available_books(type('obj', (object,), {})())
    
    elif choice == "2":
        # Search Book
        query = input("Enter book title or author to search: ").strip()
        handle_search_book(type('obj', (object,), {'query': query})())
    
    elif choice == "3":
        # Borrow Book (only for self)
        isbn = input("Enter ISBN to borrow: ").strip()
        username = current_user['username']
        handle_borrow_book(type('obj', (object,), {'username': username, 'isbn': isbn})())
    
    elif choice == "4":
        # Return Book (only for self)
        isbn = input("Enter ISBN to return: ").strip()
        username = current_user['username']
        handle_return_book(type('obj', (object,), {'username': username, 'isbn': isbn})())
    
    elif choice == "5":
        # My Borrowed Books
        handle_my_borrows(type('obj', (object,), {})())
    
    elif choice == "6":
        # Logout
        handle_logout(type('obj', (object,), {})())
    
    elif choice == "7":
        print_info("Exiting system... Thank you for using the library system.")
        sys.exit(0)
    
    else:
        print_error("Invalid choice. Please try again.")


# ==================== CLI Mode ====================

def main():
    """Main entry point."""
    # Check if any command line arguments were given
    if len(sys.argv) == 1:
        # No arguments, run interactive mode
        interactive_mode()
        return
    
    # Parse command line arguments manually
    command = None
    args = {}
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == 'register':
            command = 'register'
            i += 1
            while i < len(sys.argv) and not sys.argv[i].startswith('--'):
                i += 1
            while i < len(sys.argv):
                if sys.argv[i] == '--username':
                    args['username'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--password':
                    args['password'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--role':
                    args['role'] = sys.argv[i+1]
                    i += 2
                else:
                    i += 1
        
        elif arg == 'login':
            command = 'login'
            i += 1
            while i < len(sys.argv):
                if sys.argv[i] == '--username':
                    args['username'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--password':
                    args['password'] = sys.argv[i+1]
                    i += 2
                else:
                    i += 1
        
        elif arg == 'logout':
            command = 'logout'
            i += 1
        
        elif arg == 'add-book':
            command = 'add-book'
            i += 1
            while i < len(sys.argv):
                if sys.argv[i] == '--title':
                    args['title'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--author':
                    args['author'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--isbn':
                    args['isbn'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--copies':
                    args['copies'] = int(sys.argv[i+1])
                    i += 2
                else:
                    i += 1
        
        elif arg == 'list-books':
            command = 'list-books'
            i += 1
        
        elif arg == 'available-books':
            command = 'available-books'
            i += 1
        
        elif arg == 'delete-book':
            command = 'delete-book'
            i += 1
            while i < len(sys.argv):
                if sys.argv[i] == '--isbn':
                    args['isbn'] = sys.argv[i+1]
                    i += 2
                else:
                    i += 1
        
        elif arg == 'search-book':
            command = 'search-book'
            i += 1
            while i < len(sys.argv):
                if sys.argv[i] == '--query':
                    args['query'] = sys.argv[i+1]
                    i += 2
                else:
                    i += 1
        
        elif arg == 'borrow-book':
            command = 'borrow-book'
            i += 1
            while i < len(sys.argv):
                if sys.argv[i] == '--username':
                    args['username'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--isbn':
                    args['isbn'] = sys.argv[i+1]
                    i += 2
                else:
                    i += 1
        
        elif arg == 'return-book':
            command = 'return-book'
            i += 1
            while i < len(sys.argv):
                if sys.argv[i] == '--username':
                    args['username'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--isbn':
                    args['isbn'] = sys.argv[i+1]
                    i += 2
                else:
                    i += 1
        
        elif arg == 'my-borrows':
            command = 'my-borrows'
            i += 1
        
        elif arg == 'all-borrows':
            command = 'all-borrows'
            i += 1
        
        elif arg == 'overdue':
            command = 'overdue'
            i += 1
        
        elif arg == 'extend-borrow':
            command = 'extend-borrow'
            i += 1
            while i < len(sys.argv):
                if sys.argv[i] == '--username':
                    args['username'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--isbn':
                    args['isbn'] = sys.argv[i+1]
                    i += 2
                elif sys.argv[i] == '--days':
                    args['days'] = sys.argv[i+1]
                    i += 2
                else:
                    i += 1
        
        elif arg == 'stats':
            command = 'stats'
            i += 1
        
        elif arg == 'all-users':
            command = 'all-users'
            i += 1
        
        else:
            i += 1
    
    # Create args object
    args_obj = type('obj', (object,), args)()
    
    # Handle commands
    if command == 'register':
        handle_register(args_obj)
    elif command == 'login':
        handle_login(args_obj)
    elif command == 'logout':
        handle_logout(args_obj)
    elif command == 'add-book':
        handle_add_book(args_obj)
    elif command == 'list-books':
        handle_list_books(args_obj)
    elif command == 'available-books':
        handle_available_books(args_obj)
    elif command == 'delete-book':
        handle_delete_book(args_obj)
    elif command == 'search-book':
        handle_search_book(args_obj)
    elif command == 'borrow-book':
        handle_borrow_book(args_obj)
    elif command == 'return-book':
        handle_return_book(args_obj)
    elif command == 'my-borrows':
        handle_my_borrows(args_obj)
    elif command == 'all-borrows':
        handle_all_borrows(args_obj)
    elif command == 'overdue':
        handle_overdue(args_obj)
    elif command == 'extend-borrow':
        handle_extend_borrow(args_obj)
    elif command == 'stats':
        handle_borrow_stats(args_obj)
    elif command == 'all-users':
        handle_view_all_users(args_obj)
    else:
        # No valid command, show help
        print("Library Management System CLI")
        print("")
        print("Usage:")
        print("  python main.py                      # Run in interactive mode")
        print("")
        print("Authentication:")
        print("  python main.py register --username USER --password PASS --role ROLE")
        print("  python main.py login --username USER --password PASS")
        print("  python main.py logout")
        print("")
        print("Book Operations (Login required):")
        print("  python main.py add-book --title TITLE --author AUTHOR --isbn ISBN --copies N  # Admin only")
        print("  python main.py list-books")
        print("  python main.py available-books")
        print("  python main.py delete-book --isbn ISBN  # Admin only")
        print("  python main.py search-book --query QUERY")
        print("")
        print("Borrow Operations (Login required):")
        print("  python main.py borrow-book --username USER --isbn ISBN")
        print("  python main.py return-book --username USER --isbn ISBN")
        print("  python main.py my-borrows")
        print("")
        print("Admin/Librarian Operations (Login required):")
        print("  python main.py all-borrows")
        print("  python main.py overdue")
        print("  python main.py extend-borrow --username USER --isbn ISBN --days N")
        print("  python main.py stats")
        print("  python main.py all-users  # Admin only")


if __name__ == "__main__":
    main()

