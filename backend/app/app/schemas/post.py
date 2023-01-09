from typing import Optional, List

from pydantic import BaseModel

class PostBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class PostCreate(PostBase):
    title: str


class PostUpdate(PostBase):
    pass


class PostInDBBase(PostBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    pass


class PostDetail(PostInDBBase):
    likers_id: List
    likes: int
    dislikers_id: List
    dislikes: int


class PostInDB(PostInDBBase):
    pass
