from sqlalchemy import (
    Boolean, Column, ForeignKey,
    Integer, String, Table,
    Float
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    is_deleted = Column(Boolean, default=0, nullable=False)
    type_id = Column(Integer, ForeignKey("user_types.id", ondelete='SET NULL'))
    comment = relationship("Comment")
    liked_cafes = relationship(
        'Cafe',
        secondary='likes',
        back_populates='liked_users'
    )


class UserType(Base):
    __tablename__ = 'user_types'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(45), unique=True, nullable=False)


Table(
    'cafes_facilities', Base.metadata,
    Column('cafe_id', ForeignKey('cafes.id'), primary_key=True),
    Column('facility_id', ForeignKey('facilities.id'), primary_key=True),
)


class Cafe(Base):
    __tablename__ = 'cafes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), unique=True, index=True, nullable=False)
    address = Column(String(100), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    rep_number = Column(String(45), nullable=False)
    comment = relationship("Comment")
    facilities = relationship(
        'Facility',
        secondary='cafes_facilities',
        back_populates='cafes'
    )
    liked_users = relationship(
        'User',
        secondary='likes',
        back_populates='liked_cafes'
    )


class Facility(Base):
    __tablename__ = 'facilities'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(45), unique=True, nullable=False)
    cafes = relationship(
        'Cafe',
        secondary='cafes_facilities',
        back_populates='facilities'
    )


Table(
    'likes', Base.metadata,
    Column('cafe_id', ForeignKey('cafes.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
)


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    cafe_id = Column(Integer, ForeignKey("cafes.id", ondelete='CASCADE'))
    content = Column(String(100), nullable=False)
