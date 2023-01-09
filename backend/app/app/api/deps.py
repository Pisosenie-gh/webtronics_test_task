from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.schemas.user import UserInDBBase
from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from redis import Redis
import json


redis = Redis(host='redis', port=6379, db=0)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(user)
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def add_redis_data(id):
    redis.set(f"likes_{id}", json.dumps({"users_id": []}))
    redis.set(f"dislikes_{id}", json.dumps({"users_id": []}))


def get_redis_likes(id):
    like_posts = redis.get(f"likes_{id}")
    likers_id = json.loads(like_posts)["users_id"]

    return likers_id


def get_redis_dislikes(id):
    dislike_post = redis.get(f"dislikes_{id}")
    dislikers_id = json.loads(dislike_post)["users_id"]

    return dislikers_id


def delete_redis_data(id):

    redis.delete(f"likes_{id}")
    redis.delete(f"dislikes_{id}")


def update_redis_likes(id, data):
    redis.set(f"likes_{id}", json.dumps({"users_id": data}))


def update_redis_dislikes(id, data):
    redis.set(f"dislikes_{id}", json.dumps({"users_id": data}))


