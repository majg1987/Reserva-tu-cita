from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None
    email: str
    firstname: str | None = None
    lastname: str | None = None
    phone: int | None = None
