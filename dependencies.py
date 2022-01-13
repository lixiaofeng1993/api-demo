from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from conf.settings import SECRET_KEY, ALGORITHM
from sql_app.crud_users import get_user_by_name
from public.public import get_db
from public.exception import TokenException, InactiveException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise TokenException
    except JWTError:
        raise TokenException
    access_token = await request.app.state.redis.get(username)
    if not access_token and access_token != token:
        raise TokenException
    user = get_user_by_name(db, name=username)
    if user is None:
        raise TokenException
    if user.is_delete:
        raise InactiveException(name=username)
    return user


async def get_current_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    user = get_user_by_name(db, name=username)
    return user
