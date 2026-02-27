# 📚 CLI Library Management System

A Command-Line Interface (CLI) Library Management System built using Python.

This project demonstrates Object-Oriented Programming (OOP), JSON file persistence, authentication with password hashing, and role-based access control.

---

## 🎯 Project Objective

The goal of this project is to build a fully functional CLI-based application that allows a small library to:

- Manage books
- Register users
- Allow borrowing and returning of books
- Enforce role-based permissions
- Persist data using JSON files

This project simulates working as a startup development team building a structured software product.

---

## 🧠 Features

### 🔐 Authentication System
- User registration
- User login
- Password hashing using `hashlib`
- Role-based access control
- Logout functionality

### 👥 User Roles
- **Admin**
  - Full system access
  - Manage users
  - Manage books
  - View borrow records

- **Librarian**
  - Manage books
  - Manage borrowing and returns

- **Member**
  - View books
  - Borrow books
  - Return books

---

### 📖 Book Management
- Add new books
- Update book information
- Delete books
- View all books
- Search books
- Track available copies

Each book contains:
- Title
- Author
- ISBN
- Total copies
- Available copies

---

### 🔄 Borrowing System
- Borrow a book
- Return a book
- Prevent borrowing when no copies are available
- Automatically update available copies
- Track borrow date and due date
- Store borrowing history

---

## 🏗 Project Structure library_cli/
│
├── main.py
│
├── models/
│ ├── base_model.py
│ ├── user.py
│ ├── book.py
│ └── borrow_record.py
│
├── services/
│ ├── auth_service.py
│ ├── user_service.py
│ ├── book_service.py
│ └── borrow_service.py
│
├── utils/
│ ├── file_handler.py
│ ├── decorators.py
│ └── validators.py
│
├── data/
│ ├── users.json
│ ├── books.json
│ └── borrow_records.json
│
└── tests
