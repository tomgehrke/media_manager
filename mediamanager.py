from flask import (Flask, render_template, request,
                   redirect, url_for, jsonify, flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database_setup import Base, Media, MediaType, MediaFormat

app = Flask(__name__)

engine = create_engine('sqlite:///mediamanager.db')
Base.metadata.bind = engine
DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()
