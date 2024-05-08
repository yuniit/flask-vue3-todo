from bson.objectid import ObjectId
from app import db


class Todo:
    def __init__(self, title=None, userId=None, _id=None):
        self.title = title
        self.userId = userId
        self._id = str(ObjectId()) if _id is None else _id

    def get_by_user(self, userId):
        result = list(db.todos.find({"userId": userId}))
        return result

    def insert(self):
        result = db.todos.insert_one(self.to_dict())
        return result

    def delete(self, _id):
        result = db.todos.delete_one({"_id": _id})
        return result

    def to_dict(self):
        """Transform to dict to insert into mongo collection."""
        return {"_id": self._id, "title": self.title, "userId": self.userId}
