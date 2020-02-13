import os
import unittest
import json
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
    Test get all Actors
    """

    def test_get_actors(self):
        """Test API can get all Actors (GET request)."""
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        print (len(data['actors']))
        self.assertTrue(len(data['actors']))

    # def test_404_if_categories_url(self):
    #     """ Test API for exected errors in get categories end point """
    #     res = self.client().get('/categories/')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "Resource Not Found.")
    #
    # def test_get_paginated_questions(self):
    #     """Test API to get all questions (GET request). """
    #     res = self.client().get('/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(len(data['questions']))
    #
    # def test_404_questions_pagination_beyond_existing_pages(self):
    #     """Test API to get data beyond existing pages"""
    #     res = self.client().get('/questions?page=100')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "Resource Not Found.")
    #
    # def test_create_questions(self):
    #     """Test API to create new question for trivia """
    #     res = self.client().post('/questions',
    #                              json={
    #                                     "question": "What is chemical \
    #                                                 composition of water",
    #                                     "answer": "H2O",
    #                                     "category": 1,
    #                                     "difficulty": 2
    #                                   })
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    #
    # def test_405_create_question_not_allowed(self):
    #     """TEST API to post a question with URL that is not allowed """
    #     res = self.client().post('/questions/95',
    #                              json={
    #                                    "question": "What is chemical \
    #                                                composition of water",
    #                                    "answer": "H2O",
    #                                    "category": 1,
    #                                    "difficulty": 2
    #                                  })
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "Method Not Allowed.")
    #
    # def test_delete_question(self):
    #     """Test API to delete question for question id passed
    #     as request argument(DELETE request). """
    #     que = Question.query.filter(Question.question.ilike('%chemical%'))
    #     qid = que[0].id
    #     res = self.client().delete('/questions/'+str(que[0].id))
    #     question = Question.query.get(qid)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], qid)
    #     self.assertEqual(question, None)
    #
    # def test_422_if_question_do_not_exist(self):
    #     """Test API to delete question with question id that do not exist """
    #     res = self.client().delete('/questions/100')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "unprocessable.")
    #
    # def test_search_questions(self):
    #     """TEST API to search questions with search term as
    #      request argument """
    #     res = self.client().post('/searchQuestions',
    #                              json={"searchTerm": "title"})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['totalQuestions'])
    #
    # def test_get_questions_in_categories(self):
    #     """Test API to get questions that are in request category"""
    #     res = self.client().get('/categories/1/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['current_category'])
    #
    # def test_get_404_if_category_do_not_exist(self):
    #     """Test API to get error if request category do not exist"""
    #     res = self.client().get('/categories/10/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "Resource Not Found.")
    #
    # def test_play_trivia(self):
    #     """Test API to play 5 random trivia questions."""
    #     res = self.client().post('/quizzes', json={"previous_questions": [],
    #                                                "quiz_category": {
    #                                                                  "type":
    #                                                                  "science",
    #                                                                  "id": 1
    #                                                                  }})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['question'])
    #
    # def test_500_if_request_is_not_formed_poperly(self):
    #     """Test API for error if request JSON is not formed properly"""
    #     res = self.client().post('/quizzes', json={"previous_question": []})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "unprocessable.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
