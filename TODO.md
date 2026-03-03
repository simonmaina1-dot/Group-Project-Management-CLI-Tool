# TODO: Authentication and Role-Based Access Control Implementation

## Phase 1: Authentication System
- [x] 1.1 Update utils/decorators.py with enhanced role-based decorators
- [x] 1.2 Update services/auth_service.py with session management
- [x] 1.3 Add require_login, require_role decorators

## Phase 2: Service Layer Updates
- [x] 2.1 Update services/book_service.py with role checks (admin only for add/delete)
- [x] 2.2 Update services/borrow_service.py with librarian-only functions

## Phase 3: CLI Updates
- [x] 3.1 Update main.py with login requirements
- [x] 3.2 Implement role-based menu options
- [x] 3.3 Add access denied messages

## Phase 4: Testing
- [x] 4.1 Test registration and login
- [x] 4.2 Test admin functions
- [x] 4.3 Test librarian functions
- [x] 4.4 Test student functions

