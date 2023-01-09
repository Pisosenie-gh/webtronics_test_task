from typing import Optional, List

from pydantic import BaseModel
from .user import UserInDBBase

# Shared properties
class PostBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on post creation
class PostCreate(PostBase):
    title: str


# Properties to receive on post update
class PostUpdate(PostBase):
    pass



# Properties shared by models stored in DB
class PostInDBBase(PostBase):
    id: int
    title: str
    owner_id: int
    class Config:
        orm_mode = True


# Properties to return to client
class Post(PostInDBBase):
    pass

class PostDetail(PostInDBBase):
    likers_id: List
    likes: int
    dislikers_id: List
    dislikes: int

# Properties properties stored in DB
class PostInDB(PostInDBBase):
    pass
