def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": str(user["username"]),
            "email": str(user["email"]),
            "firstname": str(user["firstname"]),
            "lastname": str(user["lastname"]),
            "phone": str(user["phone"]),
            "disabled": bool(user["disabled"]),
            "password": str(user["password"])
            }