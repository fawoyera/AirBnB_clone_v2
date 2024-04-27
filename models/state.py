#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    from models.engine.file_storage import FileStorage
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City", cascade="all, delete, delete-orphan",
                          backref="state")

    @property
    def cities(self):
        return [city for city in FileStorage.__objects
                if (city.split(".")[0] == "City" and city.state_id == self.id)]
