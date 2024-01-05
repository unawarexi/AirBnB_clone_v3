#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class DBStorage:
    """Interacts with the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        hbnb_user = getenv("HBNB_MYSQL_USER")
        hbnb_pwd = getenv("HBNB_MYSQL_PWD")
        hbnb_host = getenv("HBNB_MYSQL_HOST")
        hbnb_db = getenv("HBNB_MYSQL_DB")
        hbnb_env = getenv("HBNB_ENV")
        url = "mysql+mysqldb://{}:{}@{}/{}".format(
            hbnb_user, hbnb_pwd, hbnb_host, hbnb_db
        )
        self.__engine = create_engine(url, pool_pre_ping=True)

        if hbnb_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(sess_factory)
        self.__session = session

    def get(self, cls, id):
        """Retrieve one object"""
        if cls is None or id is None:
            return None
        objs = self.__session.query(cls).all()
        return next((obj for obj in objs if obj.id == id), None)

    def count(self, cls=None):
        """Count the number of objects in storage"""
        return len(self.all(cls))

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
