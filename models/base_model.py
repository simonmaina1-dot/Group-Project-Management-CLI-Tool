"""Base model class for all models in the library CLI."""

# Import datetime for timestamp handling
from datetime import datetime
# Import typing for type hints
from typing import Dict, Any, Optional
# Import uuid for generating unique IDs
import uuid


class BaseModel:
    """Base class providing common attributes and methods for all models."""
    
    # Common attributes for all models
    # id: Unique identifier for each model instance
    id: str
    # created_at: Timestamp when the instance was created
    created_at: datetime
    # updated_at: Timestamp when the instance was last modified
    updated_at: datetime

    def __init__(self):
        """Initialize base model with common attributes."""
        # Generate a unique UUID for the instance
        self.id = str(uuid.uuid4())
        # Set creation timestamp to current time
        self.created_at = datetime.now()
        # Set updated timestamp to current time
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary.
        
        Returns:
            Dictionary representation of the model.
        """
        # Create dictionary with base model attributes
        return {
            'id': self.id,
            # Convert datetime to ISO format string for JSON serialization
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """
        Create model instance from dictionary.
        
        Args:
            data: Dictionary containing model data.
            
        Returns:
            Model instance.
        """
        # Create a new instance without calling __init__
        instance = cls()
        # Load data into the instance
        cls.load_from_dict(instance, data)
        return instance

    @staticmethod
    def load_from_dict(instance: 'BaseModel', data: Dict[str, Any]):
        """
        Load data into an existing model instance.
        
        Args:
            instance: Model instance to populate.
            data: Dictionary containing model data.
        """
        # Load ID if present in data
        if 'id' in data:
            instance.id = data['id']
        # Load created_at timestamp if present, convert from string if needed
        if 'created_at' in data:
            instance.created_at = data['created_at'] if isinstance(data['created_at'], datetime) else datetime.fromisoformat(data['created_at'])
        # Load updated_at timestamp if present, convert from string if needed
        if 'updated_at' in data:
            instance.updated_at = data['updated_at'] if isinstance(data['updated_at'], datetime) else datetime.fromisoformat(data['updated_at'])

    def update(self):
        """Update the updated_at timestamp."""
        # Set updated_at to current time whenever the model is modified
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        """Return string representation of the model."""
        # Return a string showing the class name and ID
        return f"{self.__class__.__name__}(id={self.id})"

