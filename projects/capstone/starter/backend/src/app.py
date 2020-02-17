import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor, ActMov
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content_Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    '''
        **************************ACTORS API ********************************
    '''

    '''
      @TODO:
      Create an endpoint to handle GET requests
      for all available actors.
    '''
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()
        act_format = [actor.format() for actor in actors]

        return jsonify({'success': True, 'actors': act_format})

    '''
    @TODO:
    Create a GET endpoint to get actors based on actor id.

    '''
    @app.route('/actordetail/<act_id>', methods=['GET'])
    @requires_auth('get:actors')
    def getActors(jwt, act_id):
        actor = Actor.query.get(act_id)
        if actor:
            return jsonify({"success": True,
                            "actor": actor.format()
                            })
        else:
            abort(404)

    '''
    @TODO:
    Create an endpoint to DELETE ACTOR using a Actor ID.

    '''

    @app.route('/actors/<int:aid>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, aid):

        ac = Actor.query.get(aid)
        if ac:
            try:
                ac.delete()
                return jsonify({"success": True,
                                "deleted": ac.id
                                })
            except Exception as e:
                print(str(e))
        else:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new ACTOR,

    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        data = request.get_json()
        new_fname = data.get('firstname', None)
        new_lname = data.get('lastname', None)
        new_age = data.get('age', None)
        new_gender = data.get('gender', None)
        new_phone = data.get('phone', None)
        new_actbio = data.get('act_bio', None)

        if (new_fname is None or new_lname is None
                or new_age is None or new_gender is None):

            abort(400)
        else:
            try:
                q = Actor(firstname=new_fname,
                          lastname=new_lname,
                          act_bio=new_actbio,
                          age=new_age,
                          gender=new_gender,
                          phone=new_phone,
                          )
                q.insert()
                return jsonify({"success": True,
                                "created": q.id})
            except Exception as e:
                print(str(e))
                abort(422)

    '''
    @TODO implement endpoint
        PATCH /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:actors' permission

    '''
    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        data = request.get_json()
        new_firstname = data.get('firstname', None)
        new_lastname = data.get('lastname', None)
        new_age = data.get('age', None)
        new_gender = data.get('gender', None)
        new_phone = data.get('phone', None)
        new_actbio = data.get('act_bio', None)
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor:
            actor.firstname = new_firstname
            actor.lastname = new_lastname
            actor.age = new_age
            actor.gender = new_gender
            actor.phone = new_phone
            actor.act_bio = new_actbio
            actor.update()
            return jsonify({"success": True,
                            "actor": actor.format()})
        else:
            abort(404)

    '''
    **************************MOVIES API ********************************
    '''
    '''
    @TODO:
    Create an endpoint to handle GET requests for movies,
    '''

    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()
        frmovies = [movie.format() for movie in movies]

        return jsonify({'success': True,
                        'movies': frmovies,
                        'total_movies': len(frmovies)
                        })

    '''
    @TODO:
    Create a GET endpoint to get movie deatol based on given movie id.
    '''
    @app.route('/movies/<int:mv_id>', methods=['GET'])
    @requires_auth('get:movies')
    def getMovies(jwt, mv_id):
        movie = Movie.query.get(mv_id)
        if movie:
            return jsonify({"success": True,
                            "movies": movie.format(),
                            })
        else:
            abort(404)

    '''
    @TODO:
    Create an endpoint to DELETE movie using a movie ID.
    '''

    @app.route('/movies/<int:mid>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, mid):

        mv = Movie.query.get(mid)
        if mv:
            try:
                mv.delete()
                return jsonify({"success": True,
                                "deleted": mv.id})
            except Exception as e:
                print(str(e))
        else:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new movie,
    '''

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        data = request.get_json()
        new_title = data.get('title', None)
        new_genres = data.get('genres', None)
        new_weblink = data.get('website_link', None)
        new_fblink = data.get('facebook_link', None)
        new_reldate = data.get('release_date', None)
        new_desc = data.get('mv_desc', None)
        new_imglink = data.get('image_link', None)
        new_seekact = data.get('seeking_actors', None)
        new_seekdesc = data.get('seeking_description', None)

        if new_title is None or new_genres is None or new_reldate is None:
            abort(400)
        else:
            try:
                q = Movie(title=new_title,
                          genres=new_genres,
                          mv_desc=new_desc,
                          seeking_actors=new_seekact,
                          seeking_description=new_seekdesc,
                          image_link=new_imglink,
                          website_link=new_weblink,
                          facebook_link=new_fblink,
                          release_date=new_reldate)
                q.insert()
                return jsonify({"success": True,
                                "created": q.id})
            except Exception as e:
                print(str(e))
                abort(422)

    '''
    @TODO implement endpoint
        PATCH /movies/<id>
            where <id> is the existing model id
    '''
    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        data = request.get_json()

        new_title = data.get('title', None)
        new_mvdesc = data.get('mv_desc', None)
        new_imagelink = data.get('image_link', None)
        new_seekingactors = data.get('seeking_actors', None)
        new_seekingdesc = data.get('seeking_description', None)
        new_genres = data.get('genres', None)
        new_weblink = data.get('website_link', None)
        new_fblink = data.get('facebook_link', None)
        new_reldate = data.get('release_date', None)
        movie = Movie.query.get(id)
        if movie:
            movie.title = new_title
            movie.mv_desc = new_mvdesc
            movie.image_link = new_imagelink
            movie.seeking_actors = new_seekingactors
            movie.seeking_description = new_seekingdesc
            movie.genres = new_genres
            movie.website_link = new_weblink
            movie.facebook_link = new_fblink
            movie.release_date = new_reldate
            movie.update()
            return jsonify({"success": True,
                            "movie": movie.format()})
        else:
            abort(404)

    '''
        ************** ACTOR_MOVIE_ASSOCIATION API *************************
    '''
    '''
    @TODO implement endpoint
        POST /actmovs
    '''
    @app.route('/actmov', methods=['POST'])
    @requires_auth('delete:actors')
    def create_actmov(jwt):
        data = request.get_json()
        new_actid = data.get('actor_id', None)
        new_mvid = data.get('movie_id', None)
        new_sd = data.get('start_date', None)
        new_ed = data.get('end_date', None)

        if (new_actid is None or new_mvid is None
                or new_sd is None or new_ed is None):
            abort(400)
        else:
            try:
                q = ActMov(actor_id=new_actid,
                           movie_id=new_mvid,
                           start_date=new_sd,
                           end_date=new_ed,
                           )
                q.insert()
                return jsonify({"success": True,
                                "created": q.id})
            except Exception as e:
                print(str(e))
                abort(422)

    '''
    @TODO:
    Create a GET endpoint to get movies based on actor id.
    '''

    @app.route('/actors/<int:act_id>/movies', methods=['GET'])
    def getMoviesByActor(act_id):
        act_movs = ActMov.query.filter(ActMov.actor_id == act_id)

        movies = []

        for am in act_movs:
            mv = Movie.query.get(am.movie_id)
            movies.append(mv)

        mv_format = [mv.format() for mv in movies]

        return jsonify({"success": True,
                        "movies": mv_format})

    '''
    @TODO:
    Create a GET endpoint to get actors working in a movie based on actor ID.
    '''

    @app.route('/movies/<int:mov_id>/actors', methods=['GET'])
    @requires_auth('delete:actors')
    def getActorsByMovie(jwt, mov_id):
        act_movs = ActMov.query.filter(ActMov.movie_id == mov_id)
        actors = []
        for am in act_movs:
            acmv = {}
            act = Actor.query.get(am.actor_id)
            acmv["actmovid"] = am.id
            acmv["aid"] = act.id
            acmv["fname"] = act.firstname
            acmv["lname"] = act.lastname
            acmv["sdate"] = am.start_date
            acmv["edate"] = am.end_date
            actors.append(acmv)

        return jsonify({"success": True,
                        "actors": actors})
    '''
    @TODO:
    Create a DELETE endpoint to delete actor movie association
    '''

    @app.route('/actmovs/<int:amid>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actmov(jwt, amid):
        am = ActMov.query.get(amid)
        if am:
            try:
                am.delete()
                return jsonify({"success": True,
                                "deleted": am.id})
            except Exception as e:
                print(str(e))
        else:
            abort(422)
    '''
    @TODO:
    Create a PATCH endpoint to edit actor movie association
    '''

    @app.route('/actmovs/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actmv(jwt, id):
        data = request.get_json()
        new_sd = data.get('start_date', None)
        new_ed = data.get('end_date', None)

        actmv = ActMov.query.filter(ActMov.id == id).one_or_none()
        if actmv:
            actmv.start_date = new_sd
            actmv.end_date = new_ed

            actmv.update()
            return jsonify({"success": True,
                            "actmv": actmv.format()})
        else:
            abort(404)

    '''
    Error Handling for API

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


app = create_app()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
