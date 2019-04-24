import os
import sys

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    func,
    create_engine,
    event
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker
)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    picture_url = Column(String(250), nullable=False, default='')
    email = Column(String(50), nullable=False, default='')


class MediaType(Base):
    __tablename__ = 'mediatype'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    description = Column(String(250), nullable=False, default='')
    fa_icon_class = Column(String(20), nullable=False, default='')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


def init_mediatype(session):
    session.add_all([
        MediaType(name='Movie', fa_icon_class='fa-film'),
        MediaType(name='TV Series', fa_icon_class='fa-tv'),
        MediaType(name='Webisode', fa_icon_class='fa-podcast'),
    ])
    session.commit()


class MediaFormat(Base):
    __tablename__ = 'mediaformat'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    description = Column(String(250), nullable=False, default='')
    fa_icon_class = Column(String(20), nullable=False, default='')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


def init_mediaformat(session):
    session.add_all([
        MediaFormat(name='File', fa_icon_class='fa-file-video'),
        MediaFormat(name='VHS', fa_icon_class='fa-play'),
        MediaFormat(name='DVD', fa_icon_class='fa-compact-disc'),
        MediaFormat(name='Blu-Ray', fa_icon_class='fa-compact-disc'),
        MediaFormat(name='Streaming', fa_icon_class='fa-stream'),
    ])
    session.commit()


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    year = Column(Integer, nullable=False, default=0)
    rating = Column(String(10), nullable=False, default='')
    runtime = Column(Integer, nullable=False, default=0)
    poster_url = Column(String(250), nullable=False, default='')
    imdb_id = Column(String(10), nullable=False, default='')
    mediatype_id = Column(Integer, ForeignKey('mediatype.id'), nullable=False)
    mediatype = relationship(MediaType)
    mediaformat_id = Column(Integer,
                            ForeignKey('mediaformat.id'), nullable=False)
    mediaformat = relationship(MediaFormat)
    created_user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    created_date = Column(DateTime(timezone=True),
                          nullable=False, default=func.now())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'rating': self.rating,
            'runtime': self.runtime,
            'poster_url': self.poster_url,
            'imdb_id': self.imdb_id,
            'mediatype_id': self.mediatype_id,
            'mediaformat_id': self.mediaformat_id,
        }


if __name__ == '__main__':
    engine = create_engine('sqlite:///mediamanager.db')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    DBSession = scoped_session(sessionmaker(bind=engine))
    session = DBSession()
    init_mediaformat(session)
    init_mediatype(session)
