import sqlalchemy
from .db_session import SqlAlchemyBase

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Departments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    user = orm.relationship('User')
