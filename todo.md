# TODO.md - CLI Library Management System

## Project Overview
Build a CLI-based Library Management System using OOP and JSON persistence for small schools and community libraries.

---

## Phase 1: Project Setup & Infrastructure

### 1.1 Create Project Folder Structure
- [x] Create main project directory: `library_cli/`
- [x] Create `models/` directory
- [x] Create `services/` directory
- [x] Create `utils/` directory
- [x] Create `data/` directory
- [x] Create `tests/` directory

### 1.2 Initialize Git Repository
- [x] Initialize git repo
- [x] Create branch: `develop`
- [x] Create feature branches:
  - `feature/auth`
  - `feature/books`
  - `feature/borrowing`
  - `feature/cli`

---

## Phase 2: Models (OOP Design)

### 2.1 BaseModel (Parent Class)
- [ ] Create `models/base_model.py`
- [ ] Add shared attributes: `id`, `created_at`
- [ ] Implement `__init__` method
- [ ] Implement `to_dict()` method
- [ ] Implement `save()` method
- [ ] Implement `from_dict()` class method

### 2.2 User Model
- [ ] Create `models/user.py` (inherits BaseModel)
- [ ] Add attributes: `username`, `password_hash`, `role`
- [ ] Implement encapsulation (private attributes)
- [ ] Add password hashing methods
- [ ] Add role validation

### 2.3 Book Model
- [ ] Create `models/book.py` (inherits BaseModel)
- [ ] Add attributes: `title`, `author`, `isbn`, `total_copies`, `available_copies`
- [ ] Implement business rule: check availability
- [ ] Add methods to update copies

### 2.4 BorrowRecord Model
- [ ] Create `models/borrow_record.py` (inherits BaseModel)
- [ ] Add attributes: `user_id`, `book_id`, `borrow_date`, `due_date`, `returned`
- [ ] Implement relationship between User and Book

---

## Phase 3: Utilities (Utils)

### 3.1 File Handler
- [ ] Create `utils/file_handler.py`
- [ ] Implement JSON read functionality
- [ ] Implement JSON write functionality
- [ ] Add error handling for file operations
- [ ] Implement data validation

### 3.2 Validators
- [ ] Create `utils/validators.py`
- [ ] Validate username format
- [ ] Validate password strength
- [ ] Validate ISBN format
- [ ] Validate date formats
- [ ] Validate role types

### 3.3 Decorators
- [ ] Create `utils/decorators.py`
- [ ] Implement `@login_required` decorator
- [ ] Implement `@admin_required` decorator
- [ ] Implement `@librarian_required` decorator
- [ ] Add role-based access control

---

## Phase 4: Services (Business Logic)

### 4.1 Auth Service (Member 1)
- [ ] Create `services/auth_service.py`
- [ ] Implement user registration
- [ ] Implement user login (password hashing)
- [ ] Implement user logout
- [ ] Implement session management
- [ ] Handle users.json CRUD operations

### 4.2 User Service (Member 1)
- [ ] Create `services/user_service.py`
- [ ] Implement get user by ID
- [ ] Implement get user by username
- [ ] Implement update user
- [ ] Implement delete user
- [ ] Implement role management

### 4.3 Book Service (Member 2)
- [ ] Create `services/book_service.py`
- [ ] Implement add book
- [ ] Implement update book
- [ ] Implement delete book
- [ ] Implement search book (by title, author, ISBN)
- [ ] Implement list all books
- [ ] Implement update availability
- [ ] Handle books.json CRUD operations

### 4.4 Borrow Service (Member 3)
- [ ] Create `services/borrow_service.py`
- [ ] Implement borrow book
- [ ] Implement return book
- [ ] Implement due date calculation
- [ ] Implement check availability before borrow
- [ ] Implement update available copies
- [ ] Implement list borrow records
- [ ] Handle borrow_records.json CRUD operations

---

## Phase 5: CLI Main Application

### 5.1 Main Entry Point
- [ ] Create `main.py`
- [ ] Implement main menu system
- [ ] Implement role-based menus
- [ ] Connect all services

### 5.2 User Interface
- [ ] Implement login prompt
- [ ] Implement registration prompt
- [ ] Implement book listing display
- [ ] Implement borrow/return prompts
- [ ] Add input validation
- [ ] Add error handling
- [ ] Add colored output (optional: rich package)

### 5.3 Integration
- [ ] Integrate auth service with CLI
- [ ] Integrate book service with CLI
- [ ] Integrate borrow service with CLI
- [ ] Test end-to-end workflows

---

## Phase 6: Testing

### 6.1 Unit Tests
- [ ] Test BaseModel
- [ ] Test User model
- [ ] Test Book model
- [ ] Test BorrowRecord model

### 6.2 Service Tests
- [ ] Test AuthService (login, registration)
- [ ] Test BookService (CRUD operations)
- [ ] Test BorrowService (borrow, return logic)

### 6.3 Decorator Tests
- [ ] Test @login_required
- [ ] Test @admin_required
- [ ] Test @librarian_required

### 6.4 Integration Tests
- [ ] Test full borrowing workflow
- [ ] Test return workflow
- [ ] Test business rules enforcement

---

## Phase 7: Optional Features (Excellence)

- [ ] Add late fee calculation
- [ ] Add book search filters
- [ ] Add sorting functionality
- [ ] Add borrowing history
- [ ] Use rich package for colored CLI
- [ ] Add logging system

---

## Phase 8: Git Collaboration

### 8.1 Branch Workflow
- [ ] Work in feature branches
- [ ] Push regularly to remote
- [ ] Open Pull Requests
- [ ] Conduct team code reviews
- [ ] Merge to develop branch

### 8.2 Documentation
- [ ] Create README.md
- [ ] Document installation steps
- [ ] Document usage instructions
- [ ] Document contribution guidelines

---

## Work Division Summary

| Member | Area | Files |
|--------|------|-------|
| Member 1 | Authentication & User System | models/user.py, services/auth_service.py, utils/decorators.py |
| Member 2 | Book Management | models/book.py, services/book_service.py |
| Member 3 | Borrowing System | models/borrow_record.py, services/borrow_service.py |
| Member 4 | CLI & Integration | main.py, utils/validators.py, tests/ |

---

## Technical Requirements Checklist

- [ ] Classes (OOP)
- [ ] Inheritance (BaseModel)
- [ ] Encapsulation (private attributes)
- [ ] CRUD operations (services + JSON)
- [ ] Authentication (auth_service)
- [ ] Decorators (role protection)
- [ ] CLI (main.py + menus)
- [ ] Error Handling (validators)
- [ ] Git collaboration (feature branches)

---

## Presentation Preparation

Be ready to explain:
- [ ] Why BaseModel was used
- [ ] Why JSON instead of database
- [ ] How decorators enforce security
- [ ] How business rules prevent errors
- [ ] How roles restrict actions
- [ ] How Git collaboration was structured

