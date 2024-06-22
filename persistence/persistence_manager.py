#!usr/bin/python3
from abc import ABC, abstractmethod


class IPersistenceManager(ABC):
    """
    Abstract interface for managing data persistence.

    This class defines abstract methods that must be implemented by a subclass to manage data persistence
    to data sources such as databases, files, or APIs.
    
    Abstract methods:
        - save(entity): Saves a new entity to the data source.
        - get(entity_id, entity_type): Retrieves an entity from the data source by its ID and type.
        - update(entity): Updates an existing entity in the data source.
        - delete(entity_id, entity_type): Deletes an entity from the data source by its ID and type.
    """

    @abstractmethod
    def save(self, entity):
        """
        Saves a new entity to the data source.
        
        Args:
            entity: The entity to save.
            
        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        pass

    @abstractmethod
    def get(self, entity_id, entity_type):
        """
        Retrieves an entity from the data source by its ID and type.
        
        Args:
            entity_id: The unique identifier of the entity.
            entity_type: The type of the entity to retrieve.
            
        Returns:
            The retrieved entity.
        
        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        pass

    @abstractmethod
    def update(self, entity):
        """
        Updates an existing entity in the data source.
        
        Args:
            entity: The entity with updated data.
            
        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        pass

    @abstractmethod
    def delete(self, entity_id, entity_type):
        """
        Deletes an entity from the data source by its ID and type.
        
        Args:
            entity_id: The unique identifier of the entity.
            entity_type: The type of the entity to delete.
            
        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        pass
