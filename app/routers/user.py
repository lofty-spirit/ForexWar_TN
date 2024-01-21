from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utilities, oauth2
from ..database import engine, get_db

router=APIRouter(
    tags=['Profile']
)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    try:
        hashed_password= utilities.hash(user.password)
        user.password=hashed_password
        new_user=models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except Exception as e:
        # Rollback the transaction in case of an error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("/users/me", response_model=schemas.UserOut)
def get_active_user(db: Session = Depends(get_db), user_id: int=Depends(oauth2.get_current_user)):
    return user_id

@router.put("/users/me", response_model=schemas.UserOut)
def update_user_me(user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    try:
        if user_update.username:
            current_user.username = user_update.username
        if user_update.full_name:
            current_user.full_name = user_update.full_name
        if user_update.email:
            current_user.email = user_update.email
        if user_update.password:
            hashed_password = utilities.hash(user_update.password)
            current_user.password = hashed_password

        # Commit the changes to the database
        db.commit()
        db.refresh(current_user)

        return current_user
    except Exception as e:
        # Rollback the transaction in case of an error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

@router.get("/users/competing", response_model=List[schemas.UserList])
def get_competing_users(db: Session = Depends(get_db), user_id: int=Depends(oauth2.get_current_user), limit: int=100):
    users = db.query(models.User).filter(models.User.status == 'competing').order_by(models.User.id.desc()).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail="No competing users found")

    return users

@router.get("/users/failed", response_model=List[schemas.UserList])
def get_failed_users(db: Session = Depends(get_db), user_id: int=Depends(oauth2.get_current_user), limit: int=100):
    users = db.query(models.User).filter(models.User.status == 'out').order_by(models.User.id.desc()).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail="No failed users found")
    return users


@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id:int, db: Session=Depends(get_db), user_id: int= Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id: {id} does not exist")
    
    return user