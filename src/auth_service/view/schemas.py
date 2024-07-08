from pydantic import BaseModel


class User(BaseModel):
    """
    This schema defines the non-sensible information of a User.
    Private information of a user is defined in the SensibleUser schema.
    """
    username: str
    email: str


class SensibleUser(User):
    """
    This schema contains private information of a User.
    - Subclass of the User class.
    This schema should be used when creating a new user.
    """
    password: str
