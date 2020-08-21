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
Handles POST request to add a movie.
This endpoint should return the id of the movie added.
'''
@app.route('/movies', methods=['POST'])
def addMovie():
  # Get request data
  data = request.get_json()
  
  # Validate request data
  if data is None:
    abort(404)

  # Get movie title and release date
  title = data.get('title', None)
  releaseDate = data.get('release_date', None)

  # Can't continue if movie title is not available.
  if title is None:
    abort(404)

  try:
    # Create a Movie object and insert movie into the table.
    movie = Movie(title=title, release_date=releaseDate)
    movie.insert()

    # Get movie id
    return jsonify({
      'success': True,
      'id': movie.id
    })
  except:
    abort(422)


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

'''
Handles POST request to add an actor.
This endpoint should return the id of the actor added.
'''
@app.route('/actors', methods=['POST'])
def addActor():
  # Get request data
  data = request.get_json()
  
  # Validate request data
  if data is None:
    abort(404)

  # Get actor name, age and gender
  name = data.get('name', None)
  age = data.get('age', None)
  gender = data.get('gender', None)

  # Can't continue if actor's name is not available.
  if name is None:
    abort(404)

  try:
    # Create an Actor object and insert actor into the table.
    actor = Actor(name=name, age=age, gender=gender)
    actor.insert()

    # Get actor id
    return jsonify({
      'success': True,
      'id': actor.id
    })
  except:
    abort(422)

'''
Root endpoint for testing.
'''
@app.route('/')
def test():
  return "Hello!"

'''
Handle errors.
'''
@app.errorhandler(404)
def resourceNotFound(error):
  return jsonify({
    'success': False,
    'error': 404,
    'message': 'Resource Not Found'
  })

@app.errorhandler(422)
def notProcessable(error):
  return jsonify({
    'success': False,
    'error': 422,
    'message': 'Not Processable'
  })

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)