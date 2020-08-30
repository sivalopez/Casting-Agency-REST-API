import os
from sqlalchemy import Column, String, Integer, DateTime, func, CheckConstraint
from flask_sqlalchemy import SQLAlchemy
import json

# Get database path from the environment variable.
database_path = os.environ.get("DATABASE_URL", "postgres://localhost:5432/casting_agency")

db = SQLAlchemy()

'''
Sets up flask application configuration for SQL Alchemy 
and binds application with SQLAlchemy service.
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db_drop_and_create_all()

'''
Drops all tables and creates them again.
Nice way to cleanup the database.
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
'''
Movie class for creating and managing movies database table.
'''
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    release_date = Column(DateTime, default=db.func.now())
    actors = db.relationship('Actor', secondary='movies_cast', backref=db.backref('movies', lazy=True))

    # repr method to print Movie object. Helpful for debugging.
    def __repr__(self):
        return f'<Movie ID: {self.id}, title: {self.title}, release_date: {self.release_date}>'

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

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
            'release_date': self.release_date
        }

'''
Actor class for creating and managing actors database table.
'''
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, CheckConstraint('age>1 and age <= 90'), nullable=False)
    gender = Column(String(20))

    # repr method to print Actor object. Helpful for debugging.
    def __repr__(self):
        return f'<Actor ID: {self.id}, name: {self.name}, age: {self.age}, gender: {self.gender}>'

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
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
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

'''
MovieCast class as a join table to maintain the many-to-many relationship
between movies and actors tables.
'''
class MoviesCast(db.Model):
    __tablename__ = 'movies_cast'

    movie_id = Column(Integer, db.ForeignKey('movies.id'), primary_key=True)
    actor_id = Column(Integer, db.ForeignKey('actors.id'), primary_key=True)

    # repr method to print MoviesCast object. Helpful for debugging.
    def __repr__(self):
        return(
            f'<MoviesCast movie_id: {self.movie_id}, actor_id: {self.actor_id}>'
        )