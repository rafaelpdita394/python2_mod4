from app import db
from app.models.models import User, Post
from sqlalchemy import select
from datetime import datetime

def user_exists(username):
    return db.session.scalars(select(User).where(User.username == username)).first() is not None

def create_user(username, password, remember=False, foto=None, bio=None):
    new_user = User(username=username, password=password, remember=remember, foto=foto, bio=bio)
    db.session.add(new_user)
    db.session.commit()

def validate_user_password(username, password):
    res = db.session.scalars(select(User).where(User.username == username)).first()
    return res and res.password == password

def create_post(body, user):
    new_post = Post(body=body, author=user)
    db.session.add(new_post)
    db.session.commit()

def get_timeline():
    stmt = select(Post).order_by(Post.timestamp.desc()).limit(5)
    return db.session.scalars(stmt).all()
