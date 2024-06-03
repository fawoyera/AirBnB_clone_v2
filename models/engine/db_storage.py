#!/usr/bin/python3
"""DBStorage Module that defines a class to manage database storage for hbnb"""


class DBStorage:
    """Class to define the new DB storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization method for DBStorage instance"""
        from models.base_model import BaseModel, Base
        from models.city import City
        from models.state import State
        import os
        from sqlalchemy import create_engine

        HBNB_MYSQL_USER = os.environ.get('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.environ.get('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.environ.get('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.environ.get('HBNB_MYSQL_DB')
        HBNB_ENV = os.environ.get('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER, HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST, HBNB_MYSQL_DB),
                                      pool_pre_ping=True)

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session for all objects in a class"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from sqlalchemy import text

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }

        if cls is None:
            query_results = self.__session.query(User, State, City, Place,
                                                 Amenity, Review).all()
        else:
            if cls.__name__ in classes:
                query_results = self.__session.query(cls).all()

        return {obj.__class__.__name__ + '.' + obj.id: obj for
                obj in query_results}

    def new(self, obj):
        """Addd object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current database session if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        from models.base_model import BaseModel, Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review
        import os
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker, scoped_session
        from sqlalchemy.ext.declarative import declarative_base

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Method to remove private session attribute self.__session"""
        self.__session.close()
