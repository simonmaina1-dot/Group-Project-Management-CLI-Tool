#!/usr/bin/env python3
"""
Library Management System - CLI Entry Point

A simple Python CLI application for managing a library system.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import register, login
from services.book_service import (
    add_book, list_books, delete_book, search_book,
    borrow_book, return_book
)


# Global state
current_user = None


def print_success(message):
    """Print success message."""
    print(f"SUCCESS: {message}")


def print_error(message):
    """Print error message."""
    print(f"ERROR: {message}")


def print_info(message):
    """Print info message."""
    print(f"INFO: {message}")


def display_books(books, title="Book List"):
    """Display books in a simple format."""
    if not books:
        print_info("No books found.")
        return
    
    print(f"\n--- {title} ---")
    for book in books:
        print(f"Title: {book.get('title', 'N/A')}")
        print(f"  Author: {book.get('author', 'N/A')}")
        print(f"  ISBN: {book.get('isbn', 'N/A')}")
        print(f"  Available: {book.get('available_copies', 0)}")
        print()


def handle_register(args):
    """Handle user registration."""
    result = register(args.username, args.password, args.role)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_login(args):
    """Handle user login."""
    global current_user
    user = login(args.username, args.password)
    if user:
        current_user = user
        print_success(f"Welcome, {user['username']} ({user['role']})")
    else:
        print_error("Invalid username or password.")


def handle_add_book(args):
    """Handle adding a book."""
    result = add_book(args.title, args.author, args.isbn, args.copies)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_list_books(args):
    """Handle listing books."""
    books = list_books()
    display_books(books, "All Books in Library")


def handle_delete_book(args):
    """Handle deleting a book."""
    result = delete_book(args.isbn)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_search_book(args):
    """Handle searching for a book."""
    books = search_book(args.query)
    if books:
        display_books(books, f"Search Results for '{args.query}'")
    else:
        print_info(f"No books found matching '{args.query}'")


def handle_borrow_book(args):
    """Handle borrowing a book."""
    result = borrow_book(args.username, args.isbn)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def handle_return_book(args):
    """Handle returning a book."""
    result = return_book(args.username, args.isbn)
    if result.get('success'):
        print_success(result.get('message'))
    else:
        print_error(result.get('message'))


def interactive_mode():
    """Run the CLI in interactive menu mode."""
    global current_user
    
    while True:
        print("\n" + "="*50)
        print("Library Management System")
        print("="*50)
        
        if current_user:
            print(f"Logged in as: {current_user['username']} ({current_user['role']})")
        else:
            print("Not logged in")
        
        print("-"*50)
        print("1. Register")
        print("2. Login")
        print("3. Add Book")
        print("4. List Books")
        print("5. Delete Book")
        print("6. Search Book")
        print("7. Borrow Book")
        print("8. Return Book")
        print("9. Logout")
        print("10. Exit")
        print("-"*50)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            role = input("Enter role (admin/librarian/student): ").strip().lower()
            handle_register(type('obj', (object,), {'username': username, 'password': password, 'role': role})())
        
        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            handle_login(type('obj', (object,), {'username': username, 'password': password})())
        
        elif choice == "3":
            if not current_user:
                print_error("Please login first.")
                continue
            title = input("Enter book title: ").strip()
            author = input("Enter author: ").strip()
            isbn = input("Enter ISBN: ").strip()
            copies = input("Enter number of copies: ").strip()
            try:
                copies = int(copies)
                handle_add_book(type('obj', (object,), {'title': title, 'author': author, 'isbn': isbn, 'copies': copies})())
            except ValueError:
                print_error("Invalid number of copies.")
        
        elif choice == "4":
            handle_list_books(type('obj', (object,), {})())
        
        elif choice == "5":
            if not current_user:
                print_error("Please login first.")
                continue
            isbn = input("Enter ISBN to delete: ").strip()
            handle_delete_book(type('obj', (object,), {'isbn': isbn})())
        
        elif choice == "6":
            query = input("Enter book title to search: ").strip()
            handle_search_book(type('obj', (object,), {'query': query})())
        
        elif choice == "7":
            if not current_user:
                print_error("Please login first.")
                continue
            isbn = input("Enter ISBN to borrow: ").strip()
            username = current_user['username']
            handle_borrow_book(type('obj', (object,), {'username': username, 'isbn': isbn})())
        
        elif choice == "8":
            if not current_user:
                print_error("Please login first.")
                continue
            isbn = input("Enter ISBN to return: ").strip()
            username = current_user['username']
            handle_return_book(type('obj', (object,), {'username': username, 'isbn': isbn})())
        
        elif choice == "9":
            current_user = None
            print_success("Logged out successfully.")
        
        elif choice == "10":
            print_info("Exiting system... Thank you for using the library system.")
            break
        
        else:
            print_error("Invalid choice. Please try again.")


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
        else:
            i += 1
    
    # Create args object
    args_obj = type('obj', (object,), args)()
    
    # Handle commands
    if command == 'register':
        handle_register(args_obj)
    elif command == 'login':
        handle_login(args_obj)
    elif command == 'add-book':
        handle_add_book(args_obj)
    elif command == 'list-books':
        handle_list_books(args_obj)
    elif command == 'delete-book':
        handle_delete_book(args_obj)
    elif command == 'search-book':
        handle_search_book(args_obj)
    elif command == 'borrow-book':
        handle_borrow_book(args_obj)
    elif command == 'return-book':
        handle_return_book(args_obj)
    else:
        # No valid command, show help
        print("Library Management System CLI")
        print("")
        print("Usage:")
        print("  python main.py                      # Run in interactive mode")
        print("  python main.py register --username USER --password PASS --role ROLE")
        print("  python main.py login --username USER --password PASS")
        print("  python main.py add-book --title TITLE --author AUTHOR --isbn ISBN --copies N")
        print("  python main.py list-books")
        print("  python main.py delete-book --isbn ISBN")
        print("  python main.py search-book --query QUERY")
        print("  python main.py borrow-book --username USER --isbn ISBN")
        print("  python main.py return-book --username USER --isbn ISBN")


if __name__ == "__main__":
    main()

