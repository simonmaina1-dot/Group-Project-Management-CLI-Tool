# CLI Library Management System

A command-line interface (CLI) based Library Management System built with Python, using Object-Oriented Programming (OOP) principles and JSON for data persistence. Designed for small schools and community libraries.

## Features

- **User Management**: User registration, login, and role-based access control (Admin, Librarian, Member)
- **Book Management**: Add, update, delete, and search books
- **Borrowing System**: Borrow and return books with due date tracking
- **JSON Persistence**: Data stored in local JSON files for simplicity
- **CLI Interface**: Clean command-line interface with role-based menus

## Project Structure

```
library_cli/
├── main.py                 # CLI entry point
├── models/                # OOP data models
│   ├── base_model.py       # Base class with shared attributes
│   ├── user.py             # User model
│   ├── book.py             # Book model
│   └── borrow_record.py    # Borrow record model
├── services/               # Business logic
│   ├── auth_service.py     # Authentication service
│   ├── user_service.py     # User management service
│   ├── book_service.py     # Book management service
│   └── borrow_service.py   # Borrowing service
├── utils/                  # Utility functions
│   ├── file_handler.py     # JSON file operations
│   ├── decorators.py       # Role-based decorators
│   └── validators.py       # Input validation
├── data/                   # JSON data files
│   ├── users.json
│   ├── books.json
│   └── borrow_records.json
└── tests/                  # Unit tests
```

## Requirements

- Python 3.x
- No external database required (uses JSON files)

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Run the application:

```bash
python main.py
```

## Usage

1. **Start the application**: Run `python main.py`
2. **Register**: Create a new account
3. **Login**: Use your credentials to access the system
4. **Role-based access**:
   - **Admin**: Full system access
   - **Librarian**: Book and borrowing management
   - **Member**: Browse and borrow books

## Development

The project uses Git feature branches:
- `develop` - Main development branch
- `feature/auth` - Authentication features
- `feature/books` - Book management features
- `feature/borrowing` - Borrowing system features
- `feature/cli` - CLI interface features

## License


