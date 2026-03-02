# Decorators for the library management system

def admin_required(func):
    """Decorator to restrict access to admin users only."""
    def wrapper(user, *args, **kwargs):
        if user.get('role') != 'admin':
            return "Access denied. Admin privileges required."
        return func(user, *args, **kwargs)
    return wrapper


def librarian_required(func):
    """Decorator to restrict access to librarian and admin users."""
    def wrapper(user, *args, **kwargs):
        if user.get('role') not in ['admin', 'librarian']:
            return "Access denied. Librarian privileges required."
        return func(user, *args, **kwargs)
    return wrapper


def logged_in_required(func):
    """Decorator to ensure user is logged in."""
    def wrapper(user, *args, **kwargs):
        if not user:
            return "Please login to access this feature."
        return func(user, *args, **kwargs)
    return wrapper

