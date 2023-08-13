#!/usr/bin/python3
"""
BaseModel class that defines all common attributes/methods for other classes
"""

import uuid
import datetime
import models


class BaseModel:
    """
    BaseModel class that defines all common attributes like
    id, created_at and updated_at for other classes
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor method for BaseModel class
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    fmt = "%Y-%m-%dT%H:%M:%S.%f"
                    set_dataTime = datetime.datetime.strptime(value, fmt)
                    self.__dict__[key] = set_dataTime
                else:
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at

            models.storage.new(self)

    def __str__(self):
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """
        updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all
        keys/values of __dict__ of the instance
        """
        class_name = self.__class__.__name__
        attribute = self.__dict__.copy()
        attribute['__class__'] = class_name
        attribute['created_at'] = self.created_at.isoformat()
        attribute['updated_at'] = self.updated_at.isoformat()
        return attribute
