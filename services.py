import datetime
import json

from sqlalchemy.orm import Session

from models.user import UserDB, AuthModel


def get_user(db: Session, email: str):
    return db.query(UserDB).where(UserDB.email == email).first()


def create_user(db: Session, user_data: AuthModel):
    user = UserDB()
    user.email = user_data.email
    user.username = user_data.username
    user.password = user_data.password
    user.created_at = datetime.datetime.now()
    user.is_active = True
    user.roles = json.dumps({
        "pay": False,
        "order": True,
        "book": True,
    })
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
