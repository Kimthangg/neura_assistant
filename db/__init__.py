"""
Database module initialization
"""
from .base_manager import BaseMongoDBManager
# The following classes are imported through base_manager to avoid circular imports
from .base_manager import ChatMongoDBManager
from .base_manager import EmailMongoDBManager
from .base_manager import MongoDBManager

__all__ = [
    'BaseMongoDBManager',
    'ChatMongoDBManager',
    'EmailMongoDBManager',
    'MongoDBManager'
]
