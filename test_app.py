import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class AgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('TEST_DATABASE_URL')
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # To send an authenticated request
        self.casting_assistant = {
            'Authorization': 'Bearer ' + os.environ.get('ASSISTANT_TOKEN')
        }
        self.casting_director = {
            'Authorization': 'Bearer ' + os.environ.get('DIRECTOR_TOKEN')
        }
        self.executive_producer = {
            'Authorization': 'Bearer ' + os.environ.get('PRODUCER_TOKEN')
        }

        # Create new_movie object (to test POST /movies)
        self.new_movie = {
            'title': 'A Quiet Place Part II',
            'release-date': '2021-04-01'
        }

        # Create new_missing_movie object (to test POST /movies)
        self.new_missing_movie = {
            'title': '',
            'release-date': ''
        }

        # Create new_actor object (to test POST /actors)
        self.new_actor = {
            'name': 'Emily Blunt',
            'age': '37',
            'gender': 'Female'
        }

        # Create new_missing_actor object (to test POST /actors)
        self.new_missing_actor = {
            'name': '',
            'age': '',
            'gender': ''
        }

        # Create update_movie object (to test PATCH /movies/1)
        self.update_movie = {
            'title': 'Split',
            'release-date': '2016-01-01'
        }

        # Create update_actor object (to test PATCH /actors/1)
        self.update_actor = {
            'name': 'James McAvoy',
            'age': '41',
            'gender': 'Male'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # TEST (Successful Operation): GET /movies
    def test_get_movies(self):
        # Store the response in the 'res' variable
        res = self.client().get('/movies', headers=self.casting_assistant)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 200
        self.assertEqual(res.status_code, 200)
        # Check the success body is true
        self.assertEqual(data['success'], True)
        # Assert true that there are movies
        self.assertTrue(data['movies'])

    # TEST (Successful Operation): GET /actors
    def test_get_actors(self):
        # Store the response in the 'res' variable
        res = self.client().get('/actors', headers=self.casting_assistant)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 200
        self.assertEqual(res.status_code, 200)
        # Check the success body is true
        self.assertEqual(data['success'], True)
        # Assert true that there are actors
        self.assertTrue(data['actors'])

    # TEST (Successful Operation): POST /movies
    def test_create_new_movie(self):
        # Store the response in the 'res' variable
        res = self.client().post('/movies', headers=self.executive_producer, json=self.new_movie)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 200
        self.assertEqual(res.status_code, 200)
        # Check the success body is true
        self.assertEqual(data['success'], True)
        # Assert true that there is a created movie
        self.assertTrue(data['movie'])

    # TEST (Expected Error): POST /movies/10 (405: Method not allowed)
    def test_405_if_movie_creation_not_allowed(self):
        # Store the response in the 'res' variable
        res = self.client().post(
            '/movies/1000', headers=self.executive_producer, json=self.new_movie)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 405
        self.assertEqual(res.status_code, 405)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Method Not Allowed')

    # TEST (Expected Error): POST /movies (403: Permission not found.)
    def test_403_if_movie_creation_not_authorized(self):
        # Store the response in the 'res' variable
        res = self.client().post('/movies', headers=self.casting_director, json=self.new_movie)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 405
        self.assertEqual(res.status_code, 403)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Permission not found.')

    # TEST (Expected Error): POST /movies (422: Unprocessable)
    def test_422_if_movie_data_is_missing(self):
        # Store the response in the 'res' variable (send json with some empty fields)
        res = self.client().post('/movies', headers=self.executive_producer,
                                 json=self.new_missing_movie)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 422
        self.assertEqual(res.status_code, 422)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Not Processable')

    # TEST (Successful Operation): POST /actors
    def test_create_new_actor(self):
        # Store the response in the 'res' variable
        res = self.client().post('/actors', headers=self.casting_director, json=self.new_actor)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 200
        self.assertEqual(res.status_code, 200)
        # Check the success body is true
        self.assertEqual(data['success'], True)
        # Assert true that there is a created actor
        self.assertTrue(data['actor'])

    # TEST (Expected Error): POST /actors/10 (405: Method not allowed)
    def test_405_if_actor_creation_not_allowed(self):
        # Store the response in the 'res' variable
        res = self.client().post(
            '/actors/1000', headers=self.casting_director, json=self.new_actor)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 405
        self.assertEqual(res.status_code, 405)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Method Not Allowed')

    # TEST (Expected Error): POST /movies (403: Permission not found.)
    def test_403_if_actor_creation_not_authorized(self):
        # Store the response in the 'res' variable
        res = self.client().post(
            '/actors/1000', headers=self.casting_assistant, json=self.new_actor)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 405
        self.assertEqual(res.status_code, 403)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Permission not found.')

    # TEST (Expected Error): POST /actors (422: Unprocessable)
    def test_422_if_actor_data_is_missing(self):
        # Store the response in the 'res' variable (send json with some empty fields)
        res = self.client().post('/actors', headers=self.casting_director,
                                 json=self.new_missing_actor)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 422
        self.assertEqual(res.status_code, 422)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Not Processable')

    # TEST (Successful Operation): PATCH /movies/1
    def test_update_movie(self):
        # Store the response in the 'res' variable
        res = self.client().patch(
            '/movies/1', headers=self.executive_producer, json=self.update_movie)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 200
        self.assertEqual(res.status_code, 200)
        # Check the success body is true
        self.assertEqual(data['success'], True)
        # Assert true that there is an updated movie
        self.assertTrue(data['movie'])

    # TEST (Expected Error): PATCH /movies (405: Method not allowed)
    def test_405_if_movie_update_not_allowed(self):
        # Store the response in the 'res' variable
        res = self.client().patch(
            '/movies', headers=self.executive_producer, json=self.update_movie)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 405
        self.assertEqual(res.status_code, 405)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Method Not Allowed')

    # TEST (Successful Operation): PATCH /actors/1
    def test_update_actor(self):
        # Store the response in the 'res' variable
        res = self.client().patch(
            '/actors/1', headers=self.casting_director, json=self.update_actor)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 200
        self.assertEqual(res.status_code, 200)
        # Check the success body is true
        self.assertEqual(data['success'], True)
        # Assert true that there is an updated movie
        self.assertTrue(data['actor'])

    # TEST (Expected Error): PATCH /actors (405: Method not allowed)
    def test_405_if_actor_update_not_allowed(self):
        # Store the response in the 'res' variable
        res = self.client().patch(
            '/actors', headers=self.casting_director, json=self.update_actor)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 405
        self.assertEqual(res.status_code, 405)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Method Not Allowed')

    # TEST (Successful Operation): DELETE /movies/2
    def test_delete_movie(self):
        # Store the response in the 'res' variable (delete movie 1)
        res = self.client().delete('/movies/2', headers=self.executive_producer)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Retrieve the movie from the database (to check if it's no longer exist)
        movie = Movie.query.get(2)

        # Check the status code is 200
        self.assertEqual(res.status_code, 200)
        # Check the success body is true
        self.assertEqual(data['success'], True)
        # Check the deleted body to be the movie id (2)
        self.assertEqual(data['deleted'], 2)
        # Check the movie no longer exist
        self.assertEqual(movie, None)

    # TEST (Expected Error): DELETE /movies/1000 (404: Resorce is not found)
    def test_404_if_movie_does_not_exist(self):
        # Store the response in the 'res' variable
        res = self.client().delete('/movies/1000', headers=self.executive_producer)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 404
        self.assertEqual(res.status_code, 404)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Resource Not Found')

    # TEST (Successful Operation): DELETE /actors/2
    def test_delete_actor(self):
        # Store the response in the 'res' variable (delete actor 2)
        res = self.client().delete('/actors/2', headers=self.casting_director)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Retrieve the actor from the database (to check if it's no longer exist)
        actor = Actor.query.get(2)

        # Check the status code is 200
        self.assertEqual(res.status_code, 200)
        # Check the success body is true
        self.assertEqual(data['success'], True)
        # Check the deleted body to be the actor id (2)
        self.assertEqual(data['deleted'], 2)
        # Check the actor no longer exist
        self.assertEqual(actor, None)

    # TEST (Expected Error): DELETE /actors/1000 (404: Resorce is not found)
    def test_404_if_actor_does_not_exist(self):
        # Store the response in the 'res' variable
        res = self.client().delete('/actors/1000', headers=self.casting_director)
        # Load the data using json.loads of the response
        data = json.loads(res.data)

        # Check the status code is 404
        self.assertEqual(res.status_code, 404)
        # Check the success body is false
        self.assertEqual(data['success'], False)
        # Check the message body
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
