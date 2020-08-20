import os
from flask import Flask, request, abort, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  return app

app = create_app()

'''
Handles GET requests for movies.
This endpoint should return a list of movies.
'''
@app.route('/movies', methods=['GET'])
def getMovies():
  movies = Movie.query.all()

  # Abort with error when there are no movies returned by the query.
  if len(movies) == 0:
    abort(404)
  
  # Format all movies.
  formatted_movies = [movie.format() for movie in movies]

  return jsonify({
    'success': True,
    'movies': formatted_movies
  })

'''
Handles GET requests for actors.
This endpoint should return a list of actors.
'''
@app.route('/actors', methods=['GET'])
def getActors():
  actors = Actor.query.all()

  # Abort with error when there are no actors returned by the query.
  if len(actors) == 0:
    abort(404)

  # Format all actors.
  formatted_actors = [actor.format() for actor in actors]

  return jsonify({
    'success': True,
    'actors': formatted_actors
  })

@app.route('/')
def test():
  return "Hello!"

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)