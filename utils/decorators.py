# Decorators for the library management system
# Provides role-based access control and authentication checks

from functools import wraps


# ==================== Role Constants ====================

class UserRole:
    """User role constants."""
    ADMIN = 'admin'
    LIBRARIAN = 'librarian'
    STUDENT = 'student'
    
    ALL_ROLES = [ADMIN, LIBRARIAN, STUDENT]


# ==================== Access Control Decorators ====================

def require_login(func):
    """
    Decorator to ensure user is logged in before accessing the function.
    
    Usage:
        @require_login
        def my_function(current_user, ...):
            ...
    """
    @wraps(func)
    def wrapper(current_user, *args, **kwargs):
        if current_user is None:
            return {'success': False, 'message': 'Please login to access this feature.', 'error_code': 'NOT_LOGGED_IN'}
        return func(current_user, *args, **kwargs)
    return wrapper


def require_role(*allowed_roles):
    """
    Decorator to restrict access to specific roles.
    
    Usage:
        @require_role('admin', 'librarian')
        def my_function(current_user, ...):
            ...
    
    Args:
        allowed_roles: Variable number of role names that are allowed access
    """
    def decorator(func):
        @wraps(func)
        def wrapper(current_user, *args, **kwargs):
            # First check if logged in
            if current_user is None:
                return {'success': False, 'message': 'Please login to access this feature.', 'error_code': 'NOT_LOGGED_IN'}
            
            # Check if user has required role
            user_role = current_user.get('role', '')
            if user_role not in allowed_roles:
                role_names = ', '.join(allowed_roles)
                return {'success': False, 'message': f'Access denied. Required role: {role_names}. Your role: {user_role}', 'error_code': 'INSUFFICIENT_PERMISSIONS'}
            
            return func(current_user, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(func):
    """
    Decorator to restrict access to admin users only.
    
    Usage:
        @admin_required
        def my_function(current_user, ...):
            ...
    """
    @wraps(func)
    def wrapper(current_user, *args, **kwargs):
        if current_user is None:
            return {'success': False, 'message': 'Please login to access this feature.', 'error_code': 'NOT_LOGGED_IN'}
        
        if current_user.get('role') != 'admin':
            return {'success': False, 'message': 'Access denied. Admin privileges required.', 'error_code': 'ADMIN_REQUIRED'}
        
        return func(current_user, *args, **kwargs)
    return wrapper


def librarian_required(func):
    """
    Decorator to restrict access to librarian and admin users.
    
    Usage:
        @librarian_required
        def my_function(current_user, ...):
            ...
    """
    @wraps(func)
    def wrapper(current_user, *args, **kwargs):
        if current_user is None:
            return {'success': False, 'message': 'Please login to access this feature.', 'error_code': 'NOT_LOGGED_IN'}
        
        user_role = current_user.get('role', '')
        if user_role not in ['admin', 'librarian']:
            return {'success': False, 'message': 'Access denied. Librarian privileges required.', 'error_code': 'LIBRARIAN_REQUIRED'}
        
        return func(current_user, *args, **kwargs)
    return wrapper


def student_only(func):
    """
    Decorator to restrict access to student users only.
    
    Usage:
        @student_only
        def my_function(current_user, ...):
            ...
    """
    @wraps(func)
    def wrapper(current_user, *args, **kwargs):
        if current_user is None:
            return {'success': False, 'message': 'Please login to access this feature.', 'error_code': 'NOT_LOGGED_IN'}
        
        if current_user.get('role') != 'student':
            return {'success': False, 'message': 'Access denied. This feature is for students only.', 'error_code': 'STUDENT_ONLY'}
        
        return func(current_user, *args, **kwargs)
    return wrapper


# ==================== Helper Functions ====================

def check_permission(current_user, required_role):
    """
    Check if current user has the required role.
    
    Args:
        current_user: The logged in user dictionary or None
        required_role: The role required to perform the action
        
    Returns:
        Tuple of (has_permission: bool, message: str)
    """
    if current_user is None:
        return False, 'Please login to access this feature.'
    
    user_role = current_user.get('role', '')
    
    if required_role == 'admin':
        if user_role != 'admin':
            return False, 'Admin privileges required.'
    elif required_role in ['admin', 'librarian']:
        if user_role not in ['admin', 'librarian']:
            return False, 'Librarian privileges required.'
    
    return True, ''


def get_user_display_info(current_user):
    """
    Get display information about the current user.
    
    Args:
        current_user: The logged in user dictionary or None
        
    Returns:
        String with user info or 'Guest'
    """
    if current_user is None:
        return 'Guest'
    
    username = current_user.get('username', 'Unknown')
    role = current_user.get('role', 'Unknown')
    return f"{username} ({role})"

