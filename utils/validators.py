# Validators for the library management system

def validate_username(username):
    """Validate username format."""
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 50:
        return False, "Username must be at most 50 characters long."
    return True, ""


def validate_password(password):
    """Validate password format."""
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def validate_role(role):
    """Validate user role."""
    valid_roles = ['admin', 'librarian', 'student']
    if role not in valid_roles:
        return False, f"Role must be one of: {', '.join(valid_roles)}"
    return True, ""


def validate_isbn(isbn):
    """Validate ISBN format (10 or 13 digits)."""
    if not isbn:
        return False, "ISBN cannot be empty."
    # Remove hyphens and spaces
    isbn_clean = isbn.replace('-', '').replace(' ', '')
    if not (len(isbn_clean) == 10 or len(isbn_clean) == 13):
        return False, "ISBN must be 10 or 13 digits."
    if not isbn_clean.isdigit():
        return False, "ISBN must contain only digits."
    return True, ""


def validate_copies(copies):
    """Validate number of copies."""
    try:
        copies = int(copies)
        if copies < 1:
            return False, "Number of copies must be at least 1."
        return True, ""
    except (ValueError, TypeError):
        return False, "Number of copies must be a valid integer."


def validate_book_data(title, author, isbn, copies):
    """Validate all book data."""
    if not title or not title.strip():
        return False, "Title cannot be empty."
    if not author or not author.strip():
        return False, "Author cannot be empty."
    
    valid, msg = validate_isbn(isbn)
    if not valid:
        return False, msg
    
    valid, msg = validate_copies(copies)
    if not valid:
        return False, msg
    
    return True, ""

