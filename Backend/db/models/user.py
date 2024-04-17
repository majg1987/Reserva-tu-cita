from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None
    username: str
    email: str
    firstname: str | None = None
    lastname: str | None = None
    phone: str | None = None
    disabled: bool

class UserInDB(User):
    password: str
