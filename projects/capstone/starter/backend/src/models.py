import os
from sqlalchemy import Column, String, Integer, create_engine
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class ActMov(db.Model):
    __tablename__ = 'act_mov'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'movie.id',
            ondelete="CASCADE"),
        nullable=False)
    actor_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'actor.id',
            ondelete="CASCADE"),
        nullable=False)
    start_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)
    end_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    act_bio = db.Column(db.String(500))
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(120))
    act_mov = db.relationship('ActMov', backref='actor', lazy=True,
                              cascade="all, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'act_bio': self.act_bio
        }


'''
Movies
'''


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    mv_desc = db.Column(db.String(500))
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    seeking_actors = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(300))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    release_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)
    act_mov = db.relationship('ActMov', backref='movie', lazy=True,
                              cascade="all, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'mv_desc': self.mv_desc,
            'genres': self.genres,
            'image_link': self.image_link,
            'seeking_actors': self.seeking_actors,
            'seeking_description': self.seeking_description,
            'website_link': self.website_link,
            'facebook_link': self.facebook_link,
            'release_date': self.release_date,
        }
