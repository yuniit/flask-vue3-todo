from app import login_manager
from flask import request, Response, jsonify
from flask_login import current_user, login_user, logout_user
from app.auth import bp
from app.models.users import User


@login_manager.user_loader
def load_user(username):
    user = User().get_by_username(username)
    if not user:
        return None
    return User(username=user["username"])


@bp.post("/login")
def login():
    if current_user.is_authenticated:
        return Response(
            "Already logged in",
            status=500,
        )

    data = request.get_json()
    user = User().get_by_username(username=data["username"])

    if user is not None and User.check_password(
        hashed_password=user["password"], password=data["password"]
    ):
        user_obj = User(user)
        login_user(user_obj)

        return jsonify(user), 200

    return Response(
        "Username or password is incorrect",
        status=400,
    )


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return "success"


@bp.post("/register")
def register():
    if current_user.is_authenticated:
        return Response(
            "User already logged in",
            status=500,
        )

    data = request.get_json()

    user = User(username=data["username"], password=data["password"])

    # Hashing password
    user.set_password(password=data["password"])

    result = user.register()

    if not result.inserted_id:
        return {"message": "Failed to register"}, 500

    return {"message": "Success", "data": {"id": result.inserted_id}}, 200
