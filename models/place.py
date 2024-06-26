#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.engine.file_storage import FileStorage
import os
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False)
                      )

HBNB_TYPE_STORAGE = os.environ.get('HBNB_TYPE_STORAGE')


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    reviews = relationship('Review', cascade="all, delete, delete-orphan",
                           backref="place")

    if HBNB_TYPE_STORAGE != 'db':
        @property
        def reviews(self):
            return [k for k in FileStorage.__objects
                    if (k.split(".")[0] == 'Reviews'
                        and k.place_id == self.id)]

    amenities = relationship('Amenity', secondary='place_amenity',
                             backref="place_amenities",
                             viewonly=False)

    if HBNB_TYPE_STORAGE != 'db':
        @property
        def amenities(self):
            return [k for k in FileStorage.__objects
                    if (k.split(".")[0] == 'Amenity'
                        and k.split(".")[1] in amenity_ids)]

        @amenities.setter
        def amenities(self, obj):
            if obj.__class__.__name__ == 'Amenity':
                amenity_ids.append(obj.id)
