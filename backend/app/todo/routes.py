from app.todo import bp
from flask import request, Response, jsonify
from app.models.todos import Todo


@bp.route("/getByUser", methods=["GET"])
def getByUser():
    if request.method == "GET":
        userId = request.args.get("userId")
        result = Todo().get_by_user(userId=userId)
        return jsonify(result), 200


@bp.route("/insert", methods=["POST"])
def insert():
    if request.method == "POST":
        data = request.get_json()
        todo = Todo(title=data["title"], userId=data["userId"])
        todo.insert()
    
        return "Success", 200


@bp.delete("/delete")
def delete():
    _id = request.args.get("_id")
    result = Todo().delete(_id=_id)
    return "Success", 200
