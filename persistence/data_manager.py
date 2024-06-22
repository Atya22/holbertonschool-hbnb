#!usr/bin/python3
from persistence.persistence_manager import IPersistenceManager
import json
import os

class DataManager(IPersistenceManager):
    """
    A concrete implementation of IPersistenceManager using in-memory storage.

    This class provides methods for saving, retrieving, updating, and deleting 
    entities in an in-memory storage dictionary. Each entity is stored based 
    on its type and a unique identifier.
    
    Attributes:
        storage (dict): A dictionary to store entities, organized by type.
    
    Methods:
        save(entity): Saves a new entity to the storage.
        get(entity_id, entity_type): Retrieves an entity by its ID and type.
        update(entity): Updates an existing entity in the storage.
        delete(entity_id, entity_type): Deletes an entity by its ID and type.
    """

    def __init__(self, file_path="data.json"):
        """
        Initializes a new instance of DataManager with an empty storage dictionary.
        """
        self.file_path = file_path
        self.storage = self.load_from_file()
