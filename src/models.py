from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Boolean, Text, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from eralchemy2 import render_er
import sys

Base = declarative_base()


user_followers = Table(
    'user_followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True)
)

post_likes = Table(
    'post_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    full_name = Column(String(100))
    profile_picture = Column(String(255))
    bio = Column(Text)
    website = Column(String(255))
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    liked_posts = relationship('Post', secondary=post_likes, back_populates='liking_users')
    following = relationship(
        'User', secondary=user_followers,
        primaryjoin=(id == user_followers.c.follower_id),
        secondaryjoin=(id == user_followers.c.followed_id),
        backref='followers'
    )

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    caption = Column(Text)
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    
   
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')
    liking_users = relationship('User', secondary=post_likes, back_populates='liked_posts')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    media_type = Column(String(20))  
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))
    order = Column(Integer)  
    
    post = relationship('Post', back_populates='media')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

if __name__ == '__main__':
    try:
        render_er(Base, 'diagram.png')
        print("✅ Diagrama ER generado exitosamente como 'diagram.png'")
    except Exception as e:
        print(f"❌ Error al generar diagrama: {str(e)}", file=sys.stderr)
        sys.exit(1)