# coding: utf-8
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Action(Base):
    __tablename__ = 'action'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)

    childservices = relationship(u'Childservice', secondary='childservice_action')


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

    tags = relationship(u'Tag', secondary='article_tag')


t_article_tag = Table(
    'article_tag', metadata,
    Column('article_id', ForeignKey(u'article.id'), primary_key=True, nullable=False),
    Column('tag_id', ForeignKey(u'tag.id'), primary_key=True, nullable=False)
)


class Childservice(Base):
    __tablename__ = 'childservice'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)


t_childservice_action = Table(
    'childservice_action', metadata,
    Column('childservice_id', ForeignKey(u'childservice.id'), primary_key=True, nullable=False),
    Column('action_id', ForeignKey(u'action.id'), primary_key=True, nullable=False)
)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    childservice_id = Column(ForeignKey(u'childservice.id'))

    childservice = relationship(u'Childservice')


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(255))
    mail = Column(String(64), unique=True)
    confirmed = Column(Boolean, nullable=False)
    role_id = Column(ForeignKey(u'roles.id'))

    role = relationship(u'Role')
