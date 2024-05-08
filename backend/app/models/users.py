from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User:
    def __init__(self, username=None, password=None, _id=None):
        self.username = username
        self.password = password
        self._id = str(ObjectId()) if _id is None else _id

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @classmethod
    def set_password(cls, password):
        """Hashing the password with Werkzeug hash generator."""
        cls.password_hash = generate_password_hash(password)

    @staticmethod
    def check_password(hashed_password, password):
        """Validating the hashed password."""
        return check_password_hash(hashed_password, password)

    def get_by_username(self, username):
        return db.users.find_one({"username": username})

    def register(self):
        result = db.users.insert_one(self.to_dict())
        print(f"{self.to_dict()} entry created.")
        return result

    def to_dict(self):
        """Transform to dict to insert into mongo collection."""
        return {
            "_id": self._id,
            "username": self.username,
            "password": self.password_hash,
        }
