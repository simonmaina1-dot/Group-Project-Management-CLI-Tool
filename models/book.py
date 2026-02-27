"""Book model for the library CLI."""

# Import Optional for type hints
from typing import Optional
# Import BaseModel from the models package
from .base_model import BaseModel


class Book(BaseModel):
    """Represents a book in the library system."""

    def __init__(self, title: str, author: str, isbn: str, genre: str = "", description: str = "", published_year: Optional[int] = None):
        """Initialize a book instance.

        Args:
            title: Title of the book
            author: Author of the book
            isbn: ISBN of the book
            genre: Genre of the book (optional)
            description: Description of the book (optional)
            published_year: Year the book was published (optional)
        """
        # Call parent class constructor to initialize id, created_at, updated_at
        super().__init__()
        # Set book-specific attributes
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.description = description
        self.published_year = published_year
        # New books are available for borrowing by default
        self.is_available = True

    def to_dict(self) -> dict:
        """Convert book to dictionary.

        Returns:
            Dictionary representation of the book.
        """
        # Get base model attributes from parent class
        data = super().to_dict()
        # Add book-specific attributes to the dictionary
        data.update({
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'genre': self.genre,
            'description': self.description,
            'published_year': self.published_year,
            'is_available': self.is_available,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Create book instance from dictionary.

        Args:
            data: Dictionary containing book data.

        Returns:
            Book instance.
        """
        # Create instance without calling __init__ to avoid required args
        instance = cls.__new__(cls)
        # Load base model attributes from the data
        BaseModel.load_from_dict(instance, data)
        # Load book-specific attributes with default values
        instance.title = data.get('title', '')
        instance.author = data.get('author', '')
        instance.isbn = data.get('isbn', '')
        instance.genre = data.get('genre', '')
        instance.description = data.get('description', '')
        instance.published_year = data.get('published_year')
        # Default to available if not specified
        instance.is_available = data.get('is_available', True)
        return instance

    def borrow(self):
        """Mark the book as borrowed."""
        # Only borrow if the book is currently available
        if self.is_available:
            # Mark as unavailable
            self.is_available = False
            # Update the updated_at timestamp
            self.update()
            return True
        # Return False if book is already borrowed
        return False

    def return_book(self):
        """Mark the book as returned."""
        # Only return if the book is currently borrowed
        if not self.is_available:
            # Mark as available
            self.is_available = True
            # Update the updated_at timestamp
            self.update()
            return True
        # Return False if book is not borrowed
        return False

    def __str__(self) -> str:
        """Return string representation of the book."""
        # Return human-readable format: "Title by Author (ISBN: ...)"
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def __repr__(self) -> str:
        """Return detailed string representation of the book."""
        # Return developer-friendly format with all key attributes
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}', available={self.is_available})"
