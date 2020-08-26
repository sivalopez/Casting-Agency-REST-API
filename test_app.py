import unittest, sys
import json
from flask_sqlalchemy import SQLAlchemy

from src.app import create_app
from src.models import setup_db, Movie, Actor

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
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        pass

    # def test_post_movies(self):
    #     newMovie = {'title': 'Whats going on?', 'release_date': '12-06-2021'}
    #     res = self.client().post('/movies', data=json.dumps(newMovie),
    #                             headers={'Content-Type': 'application/json'})
    #     self.assertEqual(res.status_code, 200)

    def test_get_movies(self):
        res = self.client().get('/movies')
        json_res = res.json
        # print('SIVA')
        print(json_res)

        self.assertEqual(res.status_code, 200)

'''
Provides command line interface to the test script.
'''
if __name__ == "__main__":
    unittest.main()