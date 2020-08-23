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
Handles PATCH requests for movies.
This endpoint edits the movie with the given details and returns the movie_id.
'''
@app.route('/movies/<movie_id>', methods=['PATCH'])
def editMovie(movie_id):
  print('editMovie() movie_id: [' + movie_id + ']')

  # Validate movie_id
  if movie_id is None:
    abort(404)

  # Get data and validate
  data = request.get_json()
  if data is None:
    abort(404)
  
  title = data.get('title', None)
  releaseDate = data.get('release_date', None)

  # Query for the movie from database and validate
  movie = Movie.query.filter_by(id=movie_id).one_or_none()
  if movie is None:
    abort(404)

  # Set movie object with the data values and update the movie.
  try:
    # Only set the object with values if they are available.
    if title is not None:
      movie.title = title
    
    if releaseDate is not None:
      movie.release_date = releaseDate
    
    movie.update()
  except:
    abort(422)

  return jsonify({
    'success': True,
    'id': movie_id
  })

'''
Handles DELETE requests for movies.
This endpoint should delete the movie and return the deleted movie_id.
'''
@app.route('/movies/<movie_id>', methods=['DELETE'])
def deleteMovie(movie_id):
  # Validate the movie_id
  if movie_id is None:
    abort(404)

  # Get movie from database and validate
  movie = Movie.query.filter_by(id=movie_id).one_or_none()
  if movie is None:
    abort(404)

  # Delete the movie
  try:
    movie.delete()
  except:
    abort(422)

  return jsonify({
    'success': True,
    'id': movie_id
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
Handles PATCH request for actors.
This endpoint updates an actor with the given values and returns actor id.
'''
@app.route('/actors/<actor_id>', methods=['PATCH'])
def editActor(actor_id):
  # Validate actor_id and data.
  if actor_id is None:
    abort(404)

  data = request.get_json()
  if data is None:
    abort(404)

  name = data.get('name', None)
  age = data.get('age', None)
  gender = data.get('gender', None)

  # Query actor_id to get actor object and validate actor object.
  try:
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
      abort(404)

    # Only update the fields that are available.
    if name is not None:
      actor.name = name
    if age is not None:
      actor.age = age
    if gender is not None:
      actor.gender = gender

    actor.update()
  except:
    abort(422)

  return jsonify({
    'success': True,
    'id': actor_id
  })

'''
Handles DELETE requests for actors.
This endpoint should delete the actor and return the deleted actor_id.
'''
@app.route('/actors/<actor_id>', methods=['DELETE'])
def deleteActor(actor_id):
  # Validate the actor_id
  if actor_id is None:
    abort(404)

  # Get actor from database and validate
  actor = Actor.query.filter_by(id=actor_id).one_or_none()
  if actor is None:
    abort(404)

  # Delete the actor
  try:
    actor.delete()
  except:
    abort(422)

  return jsonify({
    'success': True,
    'id': actor_id
  })

'''
Root endpoint for testing.
'''
@app.route('/')
def test():
  return "Hello!"

'''
Handle errors for different response codes.
'''
@app.errorhandler(400)
def badRequest(error):
  return jsonify({
    'success': False,
    'error': 400,
    'message': 'Bad Request'
  })

@app.errorhandler(404)
def resourceNotFound(error):
  return jsonify({
    'success': False,
    'error': 404,
    'message': 'Resource Not Found'
  })

@app.errorhandler(405)
def methodNotAllowed(error):
  return jsonify({
    'success': False,
    'error': 405,
    'message': 'Method Not Allowed'
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