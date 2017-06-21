import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

class Catalog(Base):
    __tablename__ = 'catalog'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name': self.name,
            'id':self.id,
        }

class CatalogList(Base):
    __tablename__ = 'catalog_list'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    menu_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)
    category = relationship(Catalog, backref=backref("catalog_list", cascade="all, delete-orphan"))
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id':self.id,
            'description':self.description
        }

engine = create_engine(
'sqlite:///catalogitem.db')
Base.metadata.create_all(engine)
