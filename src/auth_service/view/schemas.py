from pydantic import BaseModel


class User(BaseModel):
    """
    This schema contains non-sensible user informationr.
    Private information of a user is defined in the SensibleUser schema.
    """

    username: str
    email: str  # TODO


class SensibleUser(User):
    """
    This schema contains sensible user information.
    This schema should be used when creating a new user.
    - Subclass of 'User'.
    """

    password: str
