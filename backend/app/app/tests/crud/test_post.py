from sqlalchemy.orm import Session

from app import crud
from app.schemas.post import PostCreate, PostUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_post(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    post_in = PostCreate(title=title, description=description)
    user = create_random_user(db)
    post = crud.post.create_with_owner(db=db, obj_in=post_in, owner_id=user.id)
    assert post.title == title
    assert post.description == description
    assert post.owner_id == user.id


def test_get_post(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    post_in = PostCreate(title=title, description=description)
    user = create_random_user(db)
    post = crud.post.create_with_owner(db=db, obj_in=post_in, owner_id=user.id)
    stored_post = crud.post.get(db=db, id=post.id)
    assert stored_post
    assert post.id == stored_post.id
    assert post.title == stored_post.title
    assert post.description == stored_post.description
    assert post.owner_id == stored_post.owner_id


def test_update_post(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    post_in = PostCreate(title=title, description=description)
    user = create_random_user(db)
    post = crud.post.create_with_owner(db=db, obj_in=post_in, owner_id=user.id)
    description2 = random_lower_string()
    post_update = PostUpdate(description=description2)
    post2 = crud.post.update(db=db, db_obj=post, obj_in=post_update)
    assert post.id == post2.id
    assert post.title == post2.title
    assert post2.description == description2
    assert post.owner_id == post2.owner_id


def test_delete_post(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    post_in = PostCreate(title=title, description=description)
    user = create_random_user(db)
    post = crud.post.create_with_owner(db=db, obj_in=post_in, owner_id=user.id)
    post2 = crud.post.remove(db=db, id=post.id)
    post3 = crud.post.get(db=db, id=post.id)
    assert post3 is None
    assert post2.id == post.id
    assert post2.title == title
    assert post2.description == description
    assert post2.owner_id == user.id
