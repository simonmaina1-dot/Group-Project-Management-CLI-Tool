"""Book model for the library CLI."""
from typing import Optional
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
        super().__init__()
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.description = description
        self.published_year = published_year
        self.is_available = True

    def to_dict(self) -> dict:
        """Convert book to dictionary.

        Returns:
            Dictionary representation of the book.
        """
        data = super().to_dict()
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
        BaseModel.load_from_dict(instance, data)
        instance.title = data.get('title', '')
        instance.author = data.get('author', '')
        instance.isbn = data.get('isbn', '')
        instance.genre = data.get('genre', '')
        instance.description = data.get('description', '')
        instance.published_year = data.get('published_year')
        instance.is_available = data.get('is_available', True)
        return instance

    def borrow(self):
        """Mark the book as borrowed."""
        if self.is_available:
            self.is_available = False
            self.update()
            return True
        return False

    def return_book(self):
        """Mark the book as returned."""
        if not self.is_available:
            self.is_available = True
            self.update()
            return True
        return False

    def __str__(self) -> str:
        """Return string representation of the book."""
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def __repr__(self) -> str:
        """Return detailed string representation of the book."""
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}', available={self.is_available})"
