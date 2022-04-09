import datetime as dt
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hiking_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    skill = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    news = orm.relation("HikingDB", back_populates='user')


class HikingDB(SqlAlchemyBase):
    __tablename__ = 'hiking'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    place = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    difficulty_level = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    instructor_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User')


