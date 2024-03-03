from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Модель для таблицы пользователей


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy=True))

# Модель для таблицы ролей


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


# Модель для промежуточной таблицы (ассоциативной таблицы)
user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer,
                                db.ForeignKey('role.id'))
                      )
