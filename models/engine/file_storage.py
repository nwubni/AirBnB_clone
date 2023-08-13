#!/usr/bin/python3
"""
class FileStorage that serializes instances to a JSON file and
deserializes JSON file to instances:
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    serializes instances to a JSON file and
    deserializes JSON file to instances:
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns the dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        :return:
        """
        json_objects = {}
        for key, obj in FileStorage.__objects.items():
            json_objects[key] = obj.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        deserializes the JSON file to __objects
        :return:
        """
        try:
            with open(FileStorage.__file_path, 'r') as f:
                jo = json.load(f)
                for key, obj in jo.items():
                    model_name = obj["__class__"]
                    del obj["__class__"]
                    FileStorage.__objects[key] = eval(model_name + "(**obj)")
        except FileNotFoundError:
            pass
