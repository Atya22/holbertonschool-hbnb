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

    def load_from_file(self):
        """
        Loads data from the JSON file if it exists, otherwise returns an empty dictionary.
        """
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_to_file(self):
        """
        Saves the current storage dictionary to the JSON file
        """
        with open(self.file_path, "w") as file:
            json.dump(self.storage, file, indent=4, default=str)

    def save(self, entity):
        """
        Saves a new entity to the storage.

        The entity must have an 'id' field used as a unique identifier. Entities
        are stored in a nested dictionary structure, organized by their type and ID.

        Args:
            entity: The entity to be saved. It should be a dictionary-like object with
                    an 'id' key.

        Example:
            entity = {'id': '123', 'name': 'Alice'}
            data_manager.save(entity)
        """
        entity_type = type(entity).__name__
        if entity_type not in self.storage:
            self.storage[entity_type] = {}
        self.storage[entity_type][entity.id] = entity.to_dict()
        self.save_to_file()
