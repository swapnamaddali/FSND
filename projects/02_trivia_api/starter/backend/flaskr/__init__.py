import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, result):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in result]
    fin_result = questions[start:end]
    return fin_result


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route
    after completing the TODOs
    '''

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content_Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        return response

        '''
        @TODO:
        Create an endpoint to handle GET requests
        for all available categories.
      '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        cats = {}
        for c in categories:
            cats[c.id] = c.type
        return jsonify({'success': True, 'categories': cats})

        '''
        @TODO:
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom
        of the screen for three pages.
        Clicking on the page numbers should update the questions.
        '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()
        format_questions = paginate_questions(request, questions)
        if len(format_questions) == 0:
            abort(404)
        categories = Category.query.all()
        cats = {}
        for c in categories:
            cats[c.id] = c.type

        return jsonify({'success': True,
                        'questions': format_questions,
                        'total_questions': len(questions),
                        'categories': cats,
                        'current_category': 1})

        '''
        @TODO:
        Create an endpoint to DELETE question using a question ID.

        TEST: When you click the trash icon next to a question,
        the question will be removed.
        This removal will persist in the database and when
        you refresh the page.
        '''

    @app.route('/questions/<int:qid>', methods=['DELETE'])
    def delete_question(qid):
        qe = Question.query.get(qid)
        if qe:
            qe.delete()
            return jsonify({"success": True,
                            "deleted": qe.id})
        else:
            abort(422)

        '''
        @TODO:
        Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear
        at the end of the last page
        of the questions list in the "List" tab.
        '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        new_question = data.get('question', None)
        new_answer = data.get('answer', None)
        new_category = data.get('category', None)
        new_difficulty = data.get('difficulty', None)
        if new_question is None or new_answer is None or new_category is None:
            abort(400)
        else:
            try:
                q = Question(question=new_question,
                             answer=new_answer,
                             category=new_category,
                             difficulty=new_difficulty)
                q.insert()
                return jsonify({"success": True,
                               "created": q.id})
            except Exception:
                abort(422)

        '''
        @TODO:
        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
        '''

    @app.route('/searchQuestions', methods=['POST'])
    def search_questions():
        data = request.get_json()
        sch_term = data.get('searchTerm', None)
        # Used ilike to make sure search term matches irrespective of case
        que = Question.query.filter(Question.question.ilike('%'+sch_term+'%'))
        cnt = que.count()
        format_questions = [question.format() for question in que]
        return jsonify({"success": True,
                        "questions": format_questions,
                        "totalQuestions": cnt,
                        "currentCategory": None})
        '''
        @TODO:
        Create a GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
        '''

    @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def getByCategory(cat_id):
        questions = Question.query.filter(Question.category == cat_id).all()
        if questions:
            current_cat = Category.query.get(cat_id)
            format_questions = [qe.format() for qe in questions]
            return jsonify({"success": True,
                            "questions": format_questions,
                            "current_category": current_cat.type,
                            "total_questions": len(questions)})
        else:
            abort(404)

        '''
        @TODO:
        Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.

        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not.
        '''

    @app.route('/quizzes', methods=['POST'])
    def create_quiz():
        data = request.get_json()
        previous_questions = data.get('previous_questions', None)
        cat = data.get('quiz_category', None)
        try:
            if cat['id'] == 0:
                questions = Question.query.filter(Question.id.notin_
                                                  (previous_questions)
                                                  ).limit(1).all()
            else:
                questions = Question.query.filter(Question.category
                                                  == cat['id'],
                                                  Question.id.notin_
                                                  (previous_questions)
                                                  ).limit(1).all()
            if len(questions) > 0:
                result = questions[0].format()
            else:
                result = None
            return jsonify({"success": True,
                            "question": result})
        except Exception:
            abort(422)

        '''
        @TODO:
        Create error handlers for all expected errors
        including 404 and 422.
        '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False,
                        "error": 404,
                        "message": "Resource Not Found."
                        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False,
                        "error": 422,
                        "message": "unprocessable."
                        }), 422

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({"success": False,
                        "error": 400,
                        "message": "Bad Request."
                        }), 400

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({"success": False,
                        "error": 500,
                        "message": "Internal Server Error."
                        }), 500

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({"success": False,
                        "error": 405,
                        "message": "Method Not Allowed."
                        }), 405

    return app
