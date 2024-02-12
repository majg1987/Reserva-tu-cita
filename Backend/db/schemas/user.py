def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "email": str(user["email"]),
            "firstname": str(user["firstname"]),
            "lastname": str(user["lasname"]),
            "phone": int(user["phone"]),
            "password": str(user["password"]),
            "repeatpassword": str(user["repeatpassword"])
            }