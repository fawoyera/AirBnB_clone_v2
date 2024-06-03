#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import os
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


HBNB_TYPE_STORAGE = os.environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """ State class """
    from models.engine.file_storage import FileStorage
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City", cascade="all, delete, delete-orphan",
                          backref="state")

    if HBNB_TYPE_STORAGE != 'db':
        @property
        def cities(self):
            from models import storage
            return [city for key, city in storage.all().items()
                    if (key.split(".")[0] == "City" and
                        city.state_id == self.id)]
