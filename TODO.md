# TODO List - CLI Library Management System

## Phase 1: Core Models & Utilities
- [x] Create `models/base_model.py` - Base class for all models
- [x] Create `models/user.py` - User model with roles
- [x] Create `models/book.py` - Book model
- [x] Create `models/borrow_record.py` - Borrow record model

## Phase 2: Utilities
- [ ] Create `utils/file_handler.py` - JSON file read/write operations
- [ ] Create `utils/validators.py` - Input validation functions
- [ ] Create `utils/decorators.py` - Authentication and role decorators

## Phase 3: Services (Business Logic)
- [ ] Create `services/auth_service.py` - Registration, login, logout, password hashing
- [ ] Create `services/user_service.py` - User management (CRUD)
- [ ] Create `services/book_service.py` - Book management (CRUD)
- [ ] Create `services/borrow_service.py` - Borrowing and returning logic

## Phase 4: Main Application
- [ ] Create `main.py` - CLI interface with menu system
- [ ] Implement role-based menu navigation

## Phase 5: Data & Testing
- [x] Create initial JSON data files in `data/`
- [ ] Create sample data for testing
- [ ] Create `tests/` - Unit tests for models and services

## Phase 6: Documentation
- [x] Complete README.md with project overview
- [ ] Add installation and usage instructions to README
