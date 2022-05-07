from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserRecords).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

async def create_user_history(db: Session, user: schemas.UserRecord):
    db_user = models.UserRecords(
        timestamp=user.timestamp.replace(tzinfo=None),
        farm=user.farm,
        farm_network=user.farm_network,
        wallet=user.wallet,
        dollarvalue=user.dollarvalue,
        farmnetwork=user.farmnetwork
        )

    db.add(db_user)
    
    return db_user


def delete_user_history(db: Session, wallet, start, end):
    db.query(models.UserRecords).filter(and_(models.UserRecords.wallet == wallet, models.UserRecords.timestamp >= start, models.UserRecords.timestamp <= end)).delete(synchronize_session="fetch")
    return db.commit()