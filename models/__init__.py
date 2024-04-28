#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os
from models.state import State
from models.user import User
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


__all__ = ['State', 'City', 'User', 'Place', 'Amenity', 'Review', 'storage']

HBNB_TYPE_STORAGE = os.environ.get('HBNB_TYPE_STORAGE')

if HBNB_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
