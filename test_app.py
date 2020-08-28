import os, unittest, sys
import json
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from src.app import create_app
from src.models import setup_db, db_drop_and_create_all, Movie, Actor

# Read the environment variables to get tokens.
CASTING_DIRECTOR_TOKEN = os.environ.get('CASTING_DIRECTOR_TOKEN')
CASTING_DIRECTOR_EXPIRED_TOKEN = os.environ.get('CASTING_DIRECTOR_EXPIRED_TOKEN')
EXECUTIVE_PRODUCER_TOKEN = os.environ.get('EXECUTIVE_PRODUCER_TOKEN')
EXECUTIVE_PRODUCER_EXPIRED_TOKEN = os.environ.get('EXECUTIVE_PRODUCER_EXPIRED_TOKEN')

'''
Test case for Casting Agency.
'''
class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_testdb"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # Bind the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        # clear the tables after every test.
        db_drop_and_create_all()
        pass

    def test_post_movies_success(self):
        newMovie = {'title': 'Sliding Doors', 'release_date': '12-06-1998'}
       
        res = self.client().post('/movies', data=json.dumps(newMovie),
                                headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(CASTING_DIRECTOR_TOKEN)})

        json_res = res.json
        print('SL test_post_movies_success(): ' + str(res.json))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(json_res['success'])
        self.assertIsNotNone(json_res['id'])

    def test_post_movies_error(self):
        newMovie = {'title': 'Whats going on?', 'release_date': '12-06-2021'}
        res = self.client().post('/movies', data=json.dumps(newMovie),
                                headers={'Content-Type': 'application/json'})
        print('SL test_post_movies_error() res_json: ' + str(res.json))
        self.assertEqual(res.status_code, 401)
        self.assertFalse(res.json['success'])
        self.assertEqual(res.json['error'], 'missing_authorization_header')
        self.assertEqual(res.json['message'], 'Authorization header is expected.')

    def test_get_movies_success(self):
        # Add a movie so that we can get them later with GET request.
        newMovie = {'title': 'Sliding Doors', 'release_date': '12-06-1998'}
        post_res = self.client().post('/movies', data=json.dumps(newMovie),
                                headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(CASTING_DIRECTOR_TOKEN)})
        self.assertEqual(post_res.status_code, 200)
        self.assertTrue(post_res.json['success'])

        res = self.client().get('/movies')
        json_res = res.json

        self.assertEqual(res.status_code, 200)
        self.assertTrue(json_res['success'])
        self.assertGreater(len(json_res['movies']), 0)
    
    def test_get_movies_error(self):
        res = self.client().get('/movies/1')
        json_res = res.json

        self.assertEqual(res.status_code, 200)
        self.assertFalse(json_res['success'])
        self.assertEqual(json_res['error'], 405)
        self.assertEqual(json_res['message'], 'Method Not Allowed')

    def test_edit_movies_success(self):
        # Add a new movie to edit later.
        newMovie = {'title': 'Sliding Doors', 'release_date': '12-06-1998'}
        post_res = self.client().post('/movies', data=json.dumps(newMovie),
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(CASTING_DIRECTOR_TOKEN)})
        self.assertTrue(post_res.json['success'])
        movie_id = post_res.json['id']
        self.assertIsNotNone(movie_id)

        # Edit the movie
        res = self.client().patch('/movies/' + str(movie_id), data=json.dumps({'title': 'Sliding Doors Two!'}),
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(CASTING_DIRECTOR_TOKEN)})
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['success'])

    def test_edit_movies_error(self):
        # Non existent movie_id
        res = self.client().patch('/movies/99', data=json.dumps({'title': 'Sliding Doors Three!'}),
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(CASTING_DIRECTOR_TOKEN)})

        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json['success'])
        self.assertEqual(res.json['error'], 404)
        self.assertEqual(res.json['message'], 'Resource Not Found')

    def test_delete_movies_success(self):
        # Add a new movie to edit later.
        newMovie = {'title': 'Sliding Doors2', 'release_date': '12-06-1999'}
        post_res = self.client().post('/movies', data=json.dumps(newMovie),
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(EXECUTIVE_PRODUCER_TOKEN)})
        self.assertTrue(post_res.json['success'])
        movie_id = post_res.json['id']
        self.assertIsNotNone(movie_id)

        # Delete the movie.
        res = self.client().delete('/movies/' + str(movie_id),
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(EXECUTIVE_PRODUCER_TOKEN)})

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['success'])
        self.assertIsNotNone(res.json['id'])

    def test_delete_movies_error(self):
        # Delete a non-existent movie_id
        res = self.client().delete('/movies/99',
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(EXECUTIVE_PRODUCER_TOKEN)})

        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json['success'])
        self.assertEqual(res.json['error'], 404)
        self.assertEqual(res.json['message'], 'Resource Not Found')

    def test_post_actors_success(self):
        newActor = {'name': 'Stephenie Gilmore', 'age': 36, 'gender': 'Female'}
        res = self.client().post('/actors', data=json.dumps(newActor),
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(CASTING_DIRECTOR_TOKEN)})
        print('SL test_post_actors_success(): ' + str(res.json))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['success'])
        self.assertIsNotNone(res.json['id'])

    def test_post_actors_error(self):
        # There is a unique constraint on actor's name.
        # Inserting the same name will result in error.
        # Should get 422 Not Processable error.
        newActor = {'name': 'Julia Williamson', 'age': 46, 'gender': 'Female'}
        res = self.client().post('/actors', data=json.dumps(newActor),
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(CASTING_DIRECTOR_TOKEN)})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['success'])
        self.assertIsNotNone(res.json['id'])

        duplicate_res = self.client().post('/actors', data=json.dumps(newActor),
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(CASTING_DIRECTOR_TOKEN)})
        print('SL test_post_actors_error(): ' + str(duplicate_res.json))

        self.assertEqual(duplicate_res.status_code, 200)
        self.assertFalse(duplicate_res.json['success'])
        self.assertEqual(duplicate_res.json['error'], 422)
        self.assertEqual(duplicate_res.json['message'], 'Not Processable')

    def test_get_actors_success(self):
        # Add an actor before calling get actors.
        newActor = {'name': 'Julia Williamson', 'age': 46, 'gender': 'Female'}
        post_res = self.client().post('/actors', data=json.dumps(newActor),
                        headers={'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + str(CASTING_DIRECTOR_TOKEN)})
        self.assertEqual(post_res.status_code, 200)
        self.assertTrue(post_res.json['success'])

        res = self.client().get('/actors')

        print('SL test_get_actors_success(): ', str(res.json))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['success'])
        self.assertGreater(len(res.json['actors']), 0)

    def test_get_actors_error(self):
        # No data should throw 404 Not found error.
        res = self.client().get('/actors')

        print('SL test_get_actors_error(): ' + str(res.json))
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json['success'])
        self.assertEqual(res.json['error'], 404)
        self.assertEqual(res.json['message'], 'Resource Not Found')

'''
Provides command line interface to the test script.
'''
if __name__ == "__main__":
    unittest.main()