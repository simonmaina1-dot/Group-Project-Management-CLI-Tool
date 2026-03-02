# Library Management System

A fully functional Python Command-Line Interface (CLI) application for managing a library system. This project demonstrates object-oriented programming principles, modular structure, and persistent data storage.

## Features

### Core Features
- **User Authentication**: Registration and login with password hashing
- **Role-Based Access**: Three user roles (admin, librarian, student)
- **Book Management**: Add, delete, list, and search books
- **Borrow/Return System**: Borrow books and return them with due date tracking
- **Persistent Storage**: JSON file-based data persistence

### Technical Features
- Object-Oriented Programming (OOP) principles
- Multiple interacting classes with proper inheritance
- Encapsulation using @property and @setter decorators
- Class methods for object creation and retrieval
- Input validation and error handling
- Decorators for authentication and authorization
- Interactive CLI with argparse
- Optional rich library for enhanced CLI output

## Project Structure

```
library-management/
├── main.py                 # CLI entry point
├── requirements.txt        # External dependencies
├── README.md              # This file
├── models/                # Data models
│   ├── __init__.py
│   ├── user.py           # User class with OOP features
│   ├── book.py           # Book class with OOP features
│   └── borrow_record.py  # BorrowRecord class
├── services/             # Business logic
│   ├── __init__.py
│   ├── auth_service.py   # Authentication service
│   ├── book_service.py   # Book management service
│   └── borrow_service.py # Borrow/return service
├── utils/                # Helper utilities
│   ├── __init__.py
│   ├── decorators.py     # Auth decorators
│   ├── validators.py     # Input validators
│   └── file_handler.py  # JSON file operations
├── data/                 # Data storage
│   ├── users.json
│   ├── books.json
│   └── borrow_records.json
└── tests/                # Unit tests (optional)
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd library-management
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the application in interactive menu mode:
```bash
python main.py
```

Then follow the on-screen menu to:
1. Register a new user
2. Login
3. Add books
4. List all books
5. Delete books
6. Search for books
7. Borrow books
8. Return books

### Command-Line Mode

Use subcommands for direct operations:

```bash
# Register a new user
python main.py register --username john --password secret123 --role student

# Login
python main.py login --username john --password secret123

# Add a book
python main.py add-book --title "Python Basics" --author "John Doe" --isbn 1234567890 --copies 5

# List all books
python main.py list-books

# Search for a book
python main.py search-book --query "Python"

# Delete a book
python main.py delete-book --isbn 1234567890

# Borrow a book
python main.py borrow-book --username john --isbn 1234567890

# Return a book
python main.py return-book --username john --isbn 1234567890
```

## User Roles

| Role      | Permissions                                      |
|-----------|--------------------------------------------------|
| admin     | Full system access                              |
| librarian | Book management, can borrow/return             |
| student  | Can borrow and return books                     |

## OOP Principles Implemented

### Classes
- `User` - Represents library users with authentication
- `Book` - Represents books in the library
- `BorrowRecord` - Tracks book borrowing activities

### Inheritance
- `User` extends `Person` base class

### Encapsulation
- Private attributes with `_` prefix
- `@property` decorators for controlled access
- `@setter` methods with validation

### Class Methods
- `User.create_user()` - Factory method
- `Book.create_book()` - Factory method
- `Book.validate_isbn()` - Static validation

### Magic Methods
- `__str__()` and `__repr__()` for clean output
- `__eq__()` for equality comparison
- `__hash__()` for hashing

## Data Storage

Data is persisted in JSON files:
- `data/users.json` - User accounts
- `data/books.json` - Book inventory
- `data/borrow_records.json` - Borrowing history

## Validation

Input validation includes:
- Username (3-50 characters)
- Password (minimum 6 characters)
- ISBN (10 or 13 digits)
- Number of copies (positive integer)
- User role (admin/librarian/student)

## Error Handling

- Try-except blocks for file operations
- Input validation with descriptive error messages
- Graceful handling of missing/corrupted data files

## Testing

Run the application to test functionality:
```bash
python main.py
```

Use command-line mode for quick tests:
```bash
# Test adding a book
python main.py add-book --title "Test Book" --author "Test Author" --isbn 111 --copies 5
python main.py list-books
```

## Known Issues

- None currently

## Future Enhancements

- Add unit tests
- Add more CLI formatting options
- Add book categories/genres
- Add reservation system
- Add late fee calculation
- Add email notifications

## License

This project is for educational purposes.

## Author


