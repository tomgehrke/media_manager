from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)
from database_setup import (
    Base,
    User,
    Media
)

engine = create_engine('sqlite:///mediamanager.db')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()


# Create default Users
print("Adding default users...")
session.add_all([
    User(username='Tom Gehrke', email='tomgehrke@gmail.com',
         picture_url='https://lh5.googleusercontent.com/-u4JakKyonIE/AAAAAAAAAAI/AAAAAAAA7DE/6OoSnNbZ6uQ/photo.jpg'),
    User(username='Gehrke Family', email='family@digitalmonkey.net',
         picture_url='https://lh4.googleusercontent.com/-7EfUlUbLN_w/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rdKgLTySdIR6N2Cfy3hUmIE6mwPVA/mo/photo.jpg'),
])
session.commit()
print("Users added!")

# Create some Media records
print("Adding media...")
session.add_all([
    Media(title='Star Trek', year='2009', imdb_id='tt0796366', rating='PG-13',
          mediaformat_id=4, mediatype_id=1, created_user_id=1, poster_url='https://m.media-amazon.com/images/M/MV5BMjE5NDQ5OTE4Ml5BMl5BanBnXkFtZTcwOTE3NDIzMw@@._V1_SY1000_CR0,0,674,1000_AL_.jpg'),
    Media(title='Over the Top', year='1987', imdb_id='tt0093692', rating='PG',
          mediaformat_id=2, mediatype_id=1, created_user_id=1, poster_url='https://m.media-amazon.com/images/M/MV5BNmM1NDRjNGMtY2VjOS00YzYzLWJiYjAtNzlkZmM2MzRiZGRkXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX691_CR0,0,691,999_AL_.jpg'),
    Media(title='The Flash', year='2014', imdb_id='tt3107288', rating='TV-PG',
          mediaformat_id=5, mediatype_id=2, created_user_id=1, poster_url='https://m.media-amazon.com/images/M/MV5BMjI1MDAwNDM4OV5BMl5BanBnXkFtZTgwNjUwNDIxNjM@._V1_SY1000_SX800_AL_.jpg'),
    Media(title='Guardians of the Galaxy Vol. 2', year='2017', imdb_id='tt3896198', rating='PG-13',
          mediaformat_id=4, mediatype_id=1, created_user_id=1, poster_url='https://m.media-amazon.com/images/M/MV5BMTg2MzI1MTg3OF5BMl5BanBnXkFtZTgwNTU3NDA2MTI@._V1_SY1000_CR0,0,674,1000_AL_.jpg'),
    Media(title='Star Wars: Episode IV - A New Hope', year='1977', imdb_id='tt0076759', rating='PG',
          mediaformat_id=3, mediatype_id=1, created_user_id=1, poster_url='https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SY1000_CR0,0,643,1000_AL_.jpg'),
    Media(title='Fantastic Beasts and Where to Find Them', year='2016', imdb_id='', rating='',
          mediaformat_id=4, mediatype_id=1, created_user_id=2, poster_url='https://m.media-amazon.com/images/M/MV5BMjMxOTM1OTI4MV5BMl5BanBnXkFtZTgwODE5OTYxMDI@._V1_SY1000_CR0,0,674,1000_AL_.jpg'),
    Media(title='Cosmos', year='2014', imdb_id='', rating='',
          mediaformat_id=3, mediatype_id=2, created_user_id=2, poster_url='https://m.media-amazon.com/images/M/MV5BZTk5OTQyZjYtMDk3Yy00YjhmLWE2MTYtZmY4NTg1YWUzZTQ0XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_.jpg'),
    Media(title='Cobra Kai', year='2018', imdb_id='tt7221388', rating='TV-14',
          mediaformat_id=5, mediatype_id=2, created_user_id=1, poster_url=''),
    Media(title='Firefly', year='2002', imdb_id='', rating='TV-14',
          mediaformat_id=3, mediatype_id=2, created_user_id=2, poster_url='https://m.media-amazon.com/images/M/MV5BNGEzYjIzZGUtNWI5YS00Y2IzLWIzMTQtMGJhNDljZDkzYzM0XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_.jpg'),
    Media(title='Stranger Things', year='2016', imdb_id='tt4574334', rating='TV-14',
          mediaformat_id=5, mediatype_id=2, created_user_id=2, poster_url=''),
    Media(title='Hudson Hawk', year='1991', imdb_id='tt0102070', rating='R',
          mediaformat_id=1, mediatype_id=1, created_user_id=1, poster_url='https://m.media-amazon.com/images/M/MV5BNzc3OGExYzYtMGE0NS00YmVlLWEzOWQtNTZiMjkxZWMzYzQ1XkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SY1000_CR0,0,681,1000_AL_.jpg'),
    Media(title='Secret Millionaires Club', year='2011', imdb_id='tt2111011', rating='TV-Y7',
          mediaformat_id=5, mediatype_id=3, created_user_id=2, poster_url='https://m.media-amazon.com/images/M/MV5BMjIyMDU2Nzk4Nl5BMl5BanBnXkFtZTgwNTE1NzA4MTE@._V1_SY1000_CR0,0,1236,1000_AL_.jpg'),
])
session.commit()
print("Media added!")
