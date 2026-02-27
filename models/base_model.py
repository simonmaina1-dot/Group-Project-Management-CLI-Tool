"""Base model class for all models in the library CLI."""
from datetime import datetime
from typing import Dict, Any, Optional
import uuid


class BaseModel:
    """Base class providing common attributes and methods for all models."""
    
    # Common attributes for all models
    id: str
    created_at: datetime
    updated_at: datetime

    def __init__(self):
        """Initialize base model with common attributes."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary.
        
        Returns:
            Dictionary representation of the model.
        """
        return {
            'id': self.id,
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
        instance = cls()
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
        if 'id' in data:
            instance.id = data['id']
        if 'created_at' in data:
            instance.created_at = data['created_at'] if isinstance(data['created_at'], datetime) else datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            instance.updated_at = data['updated_at'] if isinstance(data['updated_at'], datetime) else datetime.fromisoformat(data['updated_at'])

    def update(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        """Return string representation of the model."""
        return f"{self.__class__.__name__}(id={self.id})"

