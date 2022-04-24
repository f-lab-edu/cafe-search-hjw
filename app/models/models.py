from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Float,
    DateTime,
    Enum,
    Text,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class User(Base, BaseMixin):
    __tablename__ = "users"

    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    is_deleted = Column(Boolean, default=0, nullable=False)
    type_id = Column(Integer, ForeignKey("user_types.id", ondelete="SET NULL"))
    comments = relationship("Comment")
    liked_cafes = relationship("Cafe", secondary="likes", back_populates="liked_users")


class UserType(Base, BaseMixin):
    __tablename__ = "user_types"

    type = Column(Enum("admin", "user"), unique=True, nullable=False)


Table(
    "cafes_facilities",
    Base.metadata,
    Column("cafe_id", ForeignKey("cafes.id"), primary_key=True),
    Column("facility_id", ForeignKey("facilities.id"), primary_key=True),
)


class Cafe(Base, BaseMixin):
    __tablename__ = "cafes"

    name = Column(String(200), nullable=False)
    address = Column(String(200), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    rep_number = Column(String(45))
    comments = relationship("Comment")
    facilities = relationship(
        "Facility", secondary="cafes_facilities", back_populates="cafes"
    )
    liked_users = relationship("User", secondary="likes", back_populates="liked_cafes")

    __table_args__ = (UniqueConstraint(name, address),)


class Facility(Base, BaseMixin):
    __tablename__ = "facilities"

    type = Column(String(45), unique=True, nullable=False)
    cafes = relationship(
        "Cafe", secondary="cafes_facilities", back_populates="facilities"
    )


Table(
    "likes",
    Base.metadata,
    Column("cafe_id", ForeignKey("cafes.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class Comment(Base, BaseMixin):
    __tablename__ = "comments"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    cafe_id = Column(Integer, ForeignKey("cafes.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
