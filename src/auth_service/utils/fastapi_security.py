from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Security variables
crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
