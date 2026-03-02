"""
User model for the Library Management System.

This module implements the User class with full OOP principles including:
- Encapsulation using @property and @setter
- Class methods for object creation/retrieval
- Proper __str__ and __repr__ methods
"""

from datetime import datetime
from typing import Optional, List, Dict
import hashlib


class Person:
    """Base class representing a person."""
    
    def __init__(self, name: str, email: str = ""):
        self._name = name
        self._email = email
        self._created_at = datetime.now()
    
    @property
    def name(self) -> str:
        """Get the person's name."""
        return self._name
    
    @name.setter
    def name(self, value: str):
        """Set the person's name with validation."""
        if not value or len(value.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        self._name = value.strip()
    
    @property
    def email(self) -> str:
        """Get the person's email."""
        return self._email
    
    @email.setter
    def email(self, value: str):
        """Set the person's email with basic validation."""
        if value and '@' not in value:
            raise ValueError("Invalid email format.")
        self._email = value
    
    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp."""
        return self._created_at
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._name}')"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._name}', email='{self._email}')"


class User(Person):
    """
    Represents a system user in the library management system.
    
    Users can have different roles:
    - admin: Full system access
    - librarian: Book management access
    - student: Borrow/return access
    
    Attributes:
        username: Unique username for login
        password: Hashed password (never stored in plain text)
        role: Determines system permissions
        borrowed_books: List of currently borrowed book ISBNs
        borrowing_history: List of past borrow records
    """
    
    # Class-level attribute to track all users
    _all_users: List[Dict] = []
    _user_id_counter: int = 0
    
    # Valid roles
    VALID_ROLES = ['admin', 'librarian', 'student']
    
    def __init__(self, username: str, password: str, role: str, email: str = ""):
        """
        Initialize a new user.
        
        Args:
            username: Unique username
            password: Plain text password (will be hashed)
            role: User role (admin/librarian/student)
            email: Optional email address
        """
        # Initialize parent class
        super().__init__(username, email)
        
        # Validate role
        if role not in self.VALID_ROLES:
            raise ValueError(f"Role must be one of: {', '.join(self.VALID_ROLES)}")
        
        # Private attributes (encapsulation)
        self._username = username
        self._password_hash = self._hash_password(password)
        self._role = role
        self._borrowed_books: List[str] = []
        self._borrowing_history: List[Dict] = []
        self._is_active = True
        self._last_login: Optional[datetime] = None
        
        # Increment class-level user ID counter
        User._user_id_counter += 1
        self._user_id = User._user_id_counter
    
    # ==================== Properties ====================
    
    @property
    def user_id(self) -> int:
        """Get the unique user ID."""
        return self._user_id
    
    @property
    def username(self) -> str:
        """Get the username."""
        return self._username
    
    @username.setter
    def username(self, value: str):
        """Set username with validation."""
        if not value or len(value.strip()) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        if len(value) > 50:
            raise ValueError("Username must be at most 50 characters long.")
        self._username = value.strip()
    
    @property
    def password(self) -> Optional[str]:
        """Get password (returns None for security)."""
        return None  # Never expose password
    
    @password.setter
    def password(self, value: str):
        """Set password with validation."""
        if not value or len(value) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self._password_hash = self._hash_password(value)
    
    @property
    def role(self) -> str:
        """Get user role."""
        return self._role
    
    @role.setter
    def role(self, value: str):
        """Set user role with validation."""
        if value not in self.VALID_ROLES:
            raise ValueError(f"Role must be one of: {', '.join(self.VALID_ROLES)}")
        self._role = value
    
    @property
    def is_active(self) -> bool:
        """Check if user account is active."""
        return self._is_active
    
    @is_active.setter
    def is_active(self, value: bool):
        """Set user active status."""
        self._is_active = bool(value)
    
    @property
    def last_login(self) -> Optional[datetime]:
        """Get last login timestamp."""
        return self._last_login
    
    @property
    def borrowed_books(self) -> List[str]:
        """Get list of currently borrowed book ISBNs (copy for encapsulation)."""
        return self._borrowed_books.copy()
    
    @property
    def borrowing_history(self) -> List[Dict]:
        """Get borrowing history (copy for encapsulation)."""
        return self._borrowing_history.copy()
    
    # ==================== Class Methods ====================
    
    @classmethod
    def _hash_password(cls, password: str) -> str:
        """
        Hash a password using SHA-256.
        
        Args:
            password: Plain text password
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @classmethod
    def create_user(cls, username: str, password: str, role: str, email: str = "") -> 'User':
        """
        Factory method to create a new user.
        
        Args:
            username: Unique username
            password: Plain text password
            role: User role
            email: Optional email
            
        Returns:
            New User instance
        """
        return cls(username, password, role, email)
    
    @classmethod
    def validate_credentials(cls, username: str, password: str) -> Optional['User']:
        """
        Validate user credentials (used for login).
        
        Args:
            username: Username to validate
            password: Plain text password
            
        Returns:
            User instance if valid, None otherwise
        """
        # This would typically load from database
        # For now, returns None - actual implementation in auth_service
        return None
    
    @classmethod
    def get_all_roles(cls) -> List[str]:
        """Get list of all valid roles."""
        return cls.VALID_ROLES.copy()
    
    # ==================== Instance Methods ====================
    
    def verify_password(self, password: str) -> bool:
        """
        Verify if provided password matches stored hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            True if password matches, False otherwise
        """
        return self._password_hash == self._hash_password(password)
    
    def update_last_login(self):
        """Update the last login timestamp to current time."""
        self._last_login = datetime.now()
    
    def borrow_book(self, isbn: str) -> bool:
        """
        Record a book borrow.
        
        Args:
            isbn: ISBN of the book being borrowed
            
        Returns:
            True if successful
        """
        if isbn not in self._borrowed_books:
            self._borrowed_books.append(isbn)
        return True
    
    def return_book(self, isbn: str) -> bool:
        """
        Record a book return.
        
        Args:
            isbn: ISBN of the book being returned
            
        Returns:
            True if successful
        """
        if isbn in self._borrowed_books:
            self._borrowed_books.remove(isbn)
            return True
        return False
    
    def add_to_history(self, record: Dict):
        """
        Add a record to borrowing history.
        
        Args:
            record: Dictionary with borrow record details
        """
        self._borrowing_history.append(record)
    
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self._role == 'admin'
    
    def is_librarian(self) -> bool:
        """Check if user has librarian or admin role."""
        return self._role in ['librarian', 'admin']
    
    def can_borrow(self) -> bool:
        """Check if user can borrow books (not students can borrow)."""
        return self._role in ['student', 'librarian', 'admin']
    
    def to_dict(self) -> Dict:
        """
        Convert user object to dictionary for JSON storage.
        
        Returns:
            Dictionary representation of the user
        """
        return {
            'user_id': self._user_id,
            'username': self._username,
            'password': self._password_hash,
            'role': self._role,
            'email': self._email,
            'name': self._name,
            'borrowed_books': self._borrowed_books,
            'borrowing_history': self._borrowing_history,
            'is_active': self._is_active,
            'last_login': self._last_login.isoformat() if self._last_login else None,
            'created_at': self._created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """
        Create a User instance from a dictionary.
        
        Args:
            data: Dictionary with user data
            
        Returns:
            User instance
        """
        user = cls(
            username=data.get('username', ''),
            password=data.get('password', ''),  # Already hashed
            role=data.get('role', 'student'),
            email=data.get('email', '')
        )
        # Restore additional attributes
        user._user_id = data.get('user_id', User._user_id_counter)
        user._borrowed_books = data.get('borrowed_books', [])
        user._borrowing_history = data.get('borrowing_history', [])
        user._is_active = data.get('is_active', True)
        
        # Restore last_login if present
        last_login = data.get('last_login')
        if last_login:
            user._last_login = datetime.fromisoformat(last_login)
        
        # Restore created_at if present
        created_at = data.get('created_at')
        if created_at:
            user._created_at = datetime.fromisoformat(created_at)
        
        return user
    
    # ==================== Magic Methods ====================
    
    def __str__(self) -> str:
        """Return string representation."""
        return f"User(username='{self._username}', role='{self._role}')"
    
    def __repr__(self) -> str:
        """Return detailed string representation."""
        return (f"User(username='{self._username}', email='{self._email}', "
                f"role='{self._role}', is_active={self._is_active})")
    
    def __eq__(self, other) -> bool:
        """Check equality based on username."""
        if not isinstance(other, User):
            return False
        return self._username == other._username
    
    def __hash__(self) -> int:
        """Return hash based on username."""
        return hash(self._username)

