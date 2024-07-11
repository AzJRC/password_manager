from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str


class SensibleUser(User):
    password: str
