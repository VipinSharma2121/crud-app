
from sqlalchemy.orm import Session
import models

def create_user(db: Session, username: str, address: str, email: str, password: str, image):
    db_user = models.User(
        username=username,
        address=address,
        email=email,
        password=password,
        image=image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
