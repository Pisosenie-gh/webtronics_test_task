from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Post, User
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Post])
def read_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Все посты
    """
    posts = crud.post.get_multi(db, skip=skip, limit=limit)

    return posts



@router.post("/", response_model=schemas.Post)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: schemas.PostCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Создание поста
    """
    post = crud.post.create_with_owner(db=db, obj_in=post_in, owner_id=current_user.id)
    deps.add_redis_data(post.id)
    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    post_in: schemas.PostUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Редактирование поста
    """

    post = crud.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if not crud.user.is_superuser(current_user) and (post.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Нет доступа")
    post = crud.post.update(db=db, db_obj=post, obj_in=post_in)
    return post


@router.get("/{id}", response_model=schemas.PostDetail)
def read_post(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Пост по ID.
    """
    post = crud.post.get(db=db, id=id)
    likers_id = deps.get_redis_likes(id)
    dislikers_id = deps.get_redis_dislikes(id)
    post.likers_id = likers_id
    post.likes = len(likers_id)
    post.dislikers_id = dislikers_id
    post.dislikes = len(dislikers_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    return post


@router.delete("/{id}", response_model=schemas.Post)
def delete_post(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Удаление поста
    """

    post = crud.post.get(db=db, id=id)

    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if not crud.user.is_superuser(current_user) and (post.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Нет доступа")

    deps.delete_redis_data(post.id)
    post = crud.post.remove(db=db, id=id)

    return post

@router.post("/posts/{post_id}/like")
def like_post(post__id: int, db: Session = Depends(deps.get_db), user: User = Depends(deps.get_current_user)):
    post = crud.post.get(db=db, id=post__id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    if post.owner_id == user.id:
        raise HTTPException(status_code=400, detail="Нельзя поставить лайк самому себе")
    likers_id = deps.get_redis_likes(post__id)
    dislikers_id = deps.get_redis_dislikes(post__id)
    if user.id in dislikers_id:
        dislikers_id.remove(user.id)
        deps.update_redis_dislikes(post__id, dislikers_id)

    if user.id in likers_id:
        raise HTTPException(status_code=400, detail="Вы уже лайкали этот пост")
    else:
        likers_id.append(user.id)
        deps.update_redis_likes(post__id,likers_id)

    return {"status": "success"}

@router.delete("/posts/{post__id}/like")
def unlike_post(post__id: int, db: Session = Depends(deps.get_db), user: User = Depends(deps.get_current_user)):
    post = crud.post.get(db=db, id=post__id)
    likers_id = deps.get_redis_likes(post__id)

    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if user.id not in likers_id:
        raise HTTPException(status_code=400, detail="Вы не лайкали этот пост")
    else:
        likers_id.remove(user.id)
        deps.update_redis_likes(post__id, likers_id)
    return {"status": "success"}

@router.post("/posts/{post_id}/dislike")
def dislike_post(post__id: int, db: Session = Depends(deps.get_db), user: User = Depends(deps.get_current_user)):

    post = crud.post.get(db=db, id=post__id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    if post.owner_id == user.id:
        raise HTTPException(status_code=400, detail="Нельзя поставить дизлайк самому себе")

    likers_id = deps.get_redis_likes(post__id)
    dislikers_id = deps.get_redis_dislikes(post__id)
    if user.id in likers_id:
        likers_id.remove(user.id)
        deps.update_redis_likes(post__id,likers_id)
    if user.id in dislikers_id:
        raise HTTPException(status_code=400, detail="Вы уже дизлайкали этот пост")
    else:
        dislikers_id.append(user.id)
        deps.update_redis_dislikes(post__id, dislikers_id)

    return {"status": "success"}


@router.delete("/posts/{post_id}/dislike")
def undislike_post(post__id: int, db: Session = Depends(deps.get_db), user: User = Depends(deps.get_current_user)):
    post = crud.post.get(db=db, id=post__id)
    dislikers_id = deps.get_redis_dislikes(post__id)

    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if user.id not in dislikers_id:
        raise HTTPException(status_code=400, detail="Вы не дизлайкали этот пост")
    else:
        dislikers_id.remove(user.id)
        deps.update_redis_dislikes(post__id, dislikers_id)
    return {"status": "success"}