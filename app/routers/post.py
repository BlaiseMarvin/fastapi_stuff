from typing import List,Optional
from fastapi import Depends,HTTPException,status,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas,models,oauth2
from sqlalchemy import func


router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

### GET ALL POSTS => psycopg2 directly and also with SQLAlchemy ###

# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts=cursor.fetchall()
#     return {"data":posts}

# ,response_model=List[schemas.PostOut]
@router.get("/")
def get_posts(db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    #print(results)
    return results

### CREATE A POST => psycopg2 directly and also with SQLAlchemy ###

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
#     cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
#     new_post=cursor.fetchone()
#     conn.commit()
#     return {"data":new_post}

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    id:int=user_id.id
    p_post=post.dict()
    p_post.update({"owner_id":id})
    new_post=models.Post(**p_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# @app.get("/posts/latest")
# def get_latest_post():
#     cursor.execute("""SELECT * FROM posts WHERE created_at=(SELECT MAX(created_at) FROM posts)""")
#     post=cursor.fetchone()
#     return {"detail":post}

### EXTRACT A POST BY ID => USING pyscopg2 and Sqlalchemy ###

# @app.get("/posts/{id}")
# def get_post(id:int):
#     cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
#     post=cursor.fetchone()
#     if not post:
#         raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
#     return {"post_detail":post}

@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return post

### DELETE A POST BY ID => USING psycopg2 and SQLALCHEMY ###

# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
#     post=cursor.fetchone()
#     if not post:
#         raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
#     else:
#         cursor.execute("""DELETE FROM posts WHERE id=%s""",(id,))
#         conn.commit()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    current_user_id=int(user_id.id)
    if not post_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    elif post_query.first().owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    else:
        post_query.delete(synchronize_session=False)
        db.commit()

#### UPDATE A POST BY ID => USING psycopg2 and SQLALCHEMY ####

# @app.put("/posts/{id}")
# def update_post(id:int,post:Post):
#     cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
#     post_exists=cursor.fetchone()
#     if not post_exists:
#         raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
#     else:
        
#         cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,id))
#         post=cursor.fetchone()
#         conn.commit()
#         return {"detail":post}

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    actual_post=post_query.first()

    if not actual_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    elif actual_post.owner_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not permitted to perform requested action")
    else:
        post_query.update(**post,synchronize_session=False)
        db.commit()
        return post_query.first()