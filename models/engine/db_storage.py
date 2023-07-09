from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = {
           'User': User, 'Place': Place,
           'State': State, 'City': City, 'Amenity': Amenity,
           'Review': Review
          }

class DBStorage:
    """
    This class manages storage of the application using a MySQL database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Constructor of the DBStorage class.
        """
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        db = f'mysql+mysqldb://{user}:{password}@{host}/{database}'

        self.__engine = create_engine(db, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        Query all objects on current database depending of the
        class name (argument cls). If cls=None, query all types of objects
        (User, State, City, Amenity, Place and Review).

        Returns:
            A dictionary of all objects in the database that match the query.
        """
        result = {}
        clases = [State, City, User, Amenity, Place, Review]
        if cls:
            query = self.__session.query(classes[cls])
            print("res:", query)
            for obj in query.all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                result[key] = obj
                print("res:", result)
        else:
            for cls in classes.keys():
                print("cls fail:", cls)
                query = self.__session.query(cls)
                #query = self.__session.query(cls)
                for obj in query.all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    result[key] = obj
        return result

    def new(self, obj):
        """
        Add the object to the current database session.

        Args:
            obj: The object to add to the session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit changes on the current database session.
        """
        print("db save")
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete given object from the current database session.

        Args:
            obj: The object to delete from the session.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database via SQLAlchemy.

        Loads the current database session (self.__session) from
        the engine (self.__engine) using a sessionmaker.
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

