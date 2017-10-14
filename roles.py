#!/usr/bin/env python
from flask_login import UserMixin, login_user
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    users = relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    password = Column(String(16))
    mail = Column(String(64), unique=True, index=True)

    role_id = Column(Integer, ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    def login(self):
        login_user(self)


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_ROLES_URI

    print(DB_ROLES_URI)

    engine = create_engine(DB_ROLES_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
