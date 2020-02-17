import os
import unittest
import json
from mock import patch
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, ActMov, Movie


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone project test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            'postgres:password@127.0.0.1:5432',
            self.database_name
        )
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test Actor endpoints
    """

    def test_get_actors(self):
        """Test API can get all Actors (GET request)."""
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_byID(self):
        """Test API can get Actors by actor ID(GET request).
        CASTING ASSISTANT can perform this action
        """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['get:actors']})
        patcher.start()
        res = self.client().get('/actordetail/499', headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI',
            'Content-Type': 'application/json'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        patcher.stop()

    def test_404_get_Actors_byID(self):
        """Test API for error if actor ID do not exist(GET request)."""
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['get:actors']})
        patcher.start()
        res = self.client().get('/actordetail/100', headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI',
            'Content-Type': 'application/json'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found.")
        patcher.stop()

    def test_create_actor(self):
        """Test API to create new actor
        CASTING DIRECTOR or EXECUTIVE PRODUCER Can perform
        """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['post:actors']})
        patcher.start()
        res = self.client().post('/actors',
                                 json={
                                     "firstname": "Cathrine",
                                     "lastname": "childs",
                                     "gender": "female",
                                     "age": 35,
                                     "phone": "6789806543",
                                     "act_bio": "Dramatic acting skills"
                                 },
                                 headers={
                                     'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                     'Content-Type': 'application/json'
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        patcher.stop()

    def test_create_actor_NotAuthorized(self):
        """Test API to create an ACTOR.
        Request cannot be performed with
         CASTINGASSISTANT permissions
        """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['get:actors']})
        patcher.start()
        res = self.client().post('/actors',
                                 json={
                                     "firstname": "Cathrine",
                                     "lastname": "childs",
                                     "gender": "female",
                                     "age": 35,
                                     "phone": "6789806543",
                                     "act_bio": "Dramatic acting skills"
                                 },
                                 headers={
                                     'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                     'Content-Type': 'application/json'
                                 })
        self.assertEqual(res.status_code, 401)
        patcher.stop()

    def test_405_create_actor_not_allowed(self):
        """TEST API to post a actors with URL that is not allowed """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['post:actors']})
        patcher.start()
        res = self.client().post('/actors/100',
                                 json={
                                     "firstname": "Samanatha",
                                     "lastname": "Desouza",
                                     "gender": "female",
                                     "age": 23,
                                     "phone": "6789806543",
                                 },
                                 headers={
                                     'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                     'Content-Type': 'application/json'
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed.")
        patcher.stop()

    def test_delete_actor(self):
        """Test API to delete actor for actor id passed
        as request argument(DELETE request).
        CASTING DIRECTOR or EXECUTIVE PRODUCER
        """
        act = Actor.query.filter(Actor.firstname.ilike('Cath%'))
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['delete:actors']})
        patcher.start()
        res = self.client().delete('/actors/' + str(act[0].id),
                                   headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI',
            'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        patcher.stop()

    def test_422_if_actor_do_not_exist(self):
        """Test API to delete actor with actor id that do not exist """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['delete:actors']})
        patcher.start()
        res = self.client().delete(
            '/actors/100',
            headers={
                'Authorization': 'Bearer eyJhbGciOiJSUzI',
                'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable.")
        patcher.stop()

    def test_patch_actor(self):
        """Test API to patch actor for actor id passed
        as request argument(PATCH request).
        CASTING DIRECTOR or EXECUTIVE PRODUCER can perform this action
        """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['patch:actors']})
        patcher.start()
        res = self.client().patch(
            '/actors/499',
            json={
                "firstname": "Samanatha",
                "lastname": "Akineni",
                "gender": "female",
                "age": 28,
                "phone": "6789806543",
                "act_bio": "Experienced and popular but \
                                            high remuneration!!!"},
            headers={
                'Authorization': 'Bearer eyJhbGciOiJSUzI',
                'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        patcher.stop()

    def test_404_patch_actor_donot_exist(self):
        """Test API to patch actor for actor id passed
        that do not exist(PATCH request). """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['patch:actors']})
        patcher.start()
        res = self.client().patch(
            '/actors/100',
            json={
                "firstname": "Samanatha",
                "lastname": "Akineni",
                "gender": "female",
                "age": 28,
                "phone": "6789806543",
            },
            headers={
                'Authorization': 'Bearer eyJhbGciOiJSUzI',
                'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found.")
        patcher.stop()

    """
    # TEST Movie endpoints
    # """

    def test_get_movies(self):
        """Test API can get all Movies (GET request)."""
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_byID(self):
        """Test API can get movies by movie ID(GET request).
        with atleast CASTING ASSISTANT permission
        """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['get:movies']})
        patcher.start()
        res = self.client().get('/movies/1000', headers={
                                'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                'Content-Type': 'application/json'
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_404_get_Movie_byID(self):
        """Test API for error if movie ID do not exist(GET request)."""
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['get:movies']})
        patcher.start()
        res = self.client().get('/movies/100', headers={
                                'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                'Content-Type': 'application/json'
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found.")

    def test_create_movie_Not_Authorized(self):
        """Test API for creating movie
        CASTING DIRECTOR with patch movies permission will get 401 error
        """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['patch:movies']})
        patcher.start()
        res = self.client().post('/movies',
                                 json={
                                     "title": "Cloudy sky",
                                     "mv_desc": "Movie is about family",
                                     "genres": "family",
                                     "release_date": "11/12/2020"
                                 },
                                 headers={
                                     'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                     'Content-Type': 'application/json'
                                 })
        self.assertEqual(res.status_code, 401)
        patcher.stop()

    def test_create_movie(self):
        """Test API for creating movie
        EXECUTIVE PRODUCER ONLY"""
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['post:movies']})
        patcher.start()
        res = self.client().post('/movies',
                                 json={
                                     "title": "Cloudy sky",
                                     "mv_desc": "Movie is about family",
                                     "genres": "family",
                                     "release_date": "11/12/2020"
                                 },
                                 headers={
                                     'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                     'Content-Type': 'application/json'
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        patcher.stop()

    def test_405_create_movie_not_allowed(self):
        """TEST API to post a movie with URL that is not allowed """
        res = self.client().post('/movies/20',
                                 json={
                                     "title": "Cloudy sky",
                                     "mv_desc": "Movie is about family",
                                     "genres": "family",
                                     "release_date": "11/12/2020"
                                 },
                                 headers={
                                     'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                     'Content-Type': 'application/json'
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method Not Allowed.")

    def test_delete_movie_Not_Authorized(self):
        """Test API to delete movie for movie id passed
        as request argument(DELETE request).
        EXECUTIVE PRODCUER only can perform this"""
        mov = Movie.query.filter(Movie.title.ilike('%Dog Life%'))
        mid = mov[0].id
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['patch:movies']})
        patcher.start()
        res = self.client().delete('/movies/' + str(mov[0].id),
                                   headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI',
            'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 401)
        patcher.stop()

    def test_delete_movie(self):
        """Test API to delete movie for movie id passed
        as request argument(DELETE request).
        EXECUTIVE PRODCUER only can perform this"""
        mov = Movie.query.filter(Movie.title.ilike('%Cloudy%'))
        mid = mov[0].id
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['delete:movies']})
        patcher.start()
        res = self.client().delete('/movies/' + str(mov[0].id),
                                   headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI',
            'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        patcher.stop()

    def test_422_if_movie_do_not_exist(self):
        """Test API to delete movie with movie id that do not exist """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['delete:movies']})
        patcher.start()
        res = self.client().delete(
            '/movies/100',
            headers={
                'Authorization': 'Bearer eyJhbGciOiJSUzI',
                'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable.")

    def test_patch_movie(self):
        """Test API to patch movie for movie id passed
        as request argument(PATCH request). """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['patch:movies']})
        patcher.start()
        res = self.client().patch(
            '/movies/1000',
            json={
                "title": "The Dog Life has purpose",
                "mv_desc": "Movie is about dog and its family",
                "genres": "family",
                "release_date": "10/12/2020"},
            headers={
                'Authorization': 'Bearer eyJhbGciOiJSUzI',
                'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        patcher.stop()
    #

    def test_404_patch_movie(self):
        """Test API for error to patch movie for movie id
        that do not exist(PATCH request). """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['patch:movies']})
        patcher.start()
        res = self.client().patch(
            '/movies/100',
            json={
                "title": "The Dog Life has purpose",
                "mv_desc": "Movie is about dog and its family",
                "genres": "family",
                "release_date": "10/12/2020"},
            headers={
                'Authorization': 'Bearer eyJhbGciOiJSUzI',
                'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found.")

    """
    ACTMOV endpoints
    """

    def test_create_actmov(self):
        """Test API for error to patch movie for movie id
        that do not exist(PATCH request). """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['delete:actors']})
        patcher.start()
        res = self.client().post('/actmov',
                                 json={
                                     "actor_id": "499",
                                     "movie_id": "1000",
                                     "start_date": "09/11/2020",
                                     "end_date": "10/11/2020"
                                 },
                                 headers={
                                     'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                     'Content-Type': 'application/json'
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_actmov_api_error_404(self):
        """Test API for error to post act movie
        with incorrect URL. """
        patcher = patch('auth.auth.verify_decode_jwt',
                        return_value={'permissions': ['delete:actors']})
        patcher.start()
        res = self.client().post('/actmov/23',
                                 json={
                                     "actor_id": "499",
                                     "movie_id": "1000",
                                     "start_date": "09/11/2020",
                                     "end_date": "10/11/2020"
                                 },
                                 headers={
                                     'Authorization': 'Bearer eyJhbGciOiJSUzI',
                                     'Content-Type': 'application/json'
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found.")


if __name__ == "__main__":
    unittest.main()
