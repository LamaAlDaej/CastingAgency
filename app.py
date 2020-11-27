import os
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth
import json

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app) # to setup the database
  CORS(app)

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

  # This endpoint shows a welcome message
  @app.route('/')
  def index():
    return jsonify({
      'message': 'Welcome to our Casting Agency!'
      }), 200
    #return render_template('home.html')

  # This endpoint RETRIEVES all movies
  @app.route('/movies') # The default method is GET
  # Require the 'get:movies' permission
  @requires_auth('get:movies')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it
  def get_movies(payload):
    # Retrieve all movies from the database
    movies = Movie.query.all()
    moviesList = []
    for movie in movies:
      # Add the movie to the list
        moviesList.append({"id": movie.id, "title": movie.title, "release_date": movie.release_date})
      
    # Return a status code 200 and json of movie's details and set the success message to true
    return jsonify({
        'success': True,
        'movies': moviesList
      }), 200 
    #return render_template('show_movies.html', movies=moviesList)


  # This endpoint RETRIEVES all actors
  @app.route('/actors') # The default method is GET
  # Require the 'get:actors' permission
  @requires_auth('get:actors')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it 
  def get_actors(payload):
    # Retrieve all actors from the database
    actors = Actor.query.all()
    actorsList = []
    for actor in actors:
      # Add the actor to the list
        actorsList.append({"id": actor.id, "name": actor.name, "age": actor.age, "gender": actor.gender})
    
    # Return a status code 200 and json of actor's details and set the success message to true
    return jsonify({
        'success': True,
        'actors': [actorsList]
      }), 200  
    #return render_template('show_actors.html', actors=actorsList)

  """
  # This endpoint redirects the user to the new movie form
  @app.route('/movies/create', methods=['GET'])
  # Require the 'post:movies' permission
  @requires_auth('post:movies')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it 
  def create_movie_form(payload):
    return render_template('new_movie.html')
  """

  # This endpoint CREATES a new movie
  @app.route('/movies', methods=['POST']) # Set the method to POST
  # Require the 'post:movies' permission
  @requires_auth('post:movies')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it 
  def add_movie(payload):
    body = request.get_json()
    # Store the form data to variables
    new_title = body['title']
    new_release_date = body['release-date']

    """
    # Store the form data to variables
    if body is None:
      new_title = request.form['title']
      new_release_date = request.form['release-date']
    else:
      new_title = body['title']
      new_release_date = body['release-date']
    """

    # Check if the user filled the fields or not
    if (not new_title) or (not new_release_date):
      # If at least one of the fields is empty, send an error (unprocessable - 422) since they're required
      abort(422)
    
    try:
      # Create an instance of the Movie model with the form data
      movie = Movie(title=new_title,release_date=new_release_date)
      # Insert the new movie to the database
      movie.insert()

      # Return a status code 200 and json of movie's details and set the success message to true
      return jsonify({
          'success': True,
          'movie': movie.format()
        }), 200  
      #return render_template('home.html') 
    
    except:
      # If an error occured while proccessing the INSERT, send an error (unprocessable - 422)
      abort(422)

  """
  # This endpoint redirects the user to the new actor form
  @app.route('/actors/create', methods=['GET'])
  # Require the 'post:actors' permission
  @requires_auth('post:actors')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it 
  def create_actor_form(payload):
    return render_template('new_actor.html')
  """
  
  # This endpoint CREATES a new actor
  @app.route('/actors', methods=['POST']) # Set the method to POST
  # Require the 'post:actors' permission
  @requires_auth('post:actors')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it 
  def add_actor(payload):
    body = request.get_json()
    # Store the form data to variables
    new_name = body['name']
    new_age = body['age']
    new_gender = body['gender'] 

    """
    if body is None:
      new_name = request.form['name']
      new_age = request.form['age']
      new_gender = request.form['gender']
    else:
      new_name = body['name']
      new_age = body['age']
      new_gender = body['gender']
    """
      
    # Check if the user filled the fields or not
    if (not new_name) or (not new_age) or (not new_gender):
      # If at least one of the fields is empty, send an error (unprocessable - 422) since they're required
      abort(422)
    
    try:
      # Create an instance of the Actor model with the form data
      actor = Actor(name=new_name,age=new_age,gender=new_gender)
      # Insert the new Actor to the database
      actor.insert()

      # Return a status code 200 and json of actor's details and set the success message to true
      return jsonify({
          'success': True,
          'actor': actor.format()
        }), 200   
      #return render_template('home.html') 
    
    except:
      # If an error occured while proccessing the INSERT, send an error (unprocessable - 422)
      abort(422)

  # This endpoint UPDATES a specified movie
  @app.route('/movies/<int:id>', methods=['PATCH'])
  # Require the 'patch:movies' permission
  @requires_auth('patch:movies')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it
  def update_movie(payload, id):
      # Retrieve the specified movie from the database by its ID
      movie = Movie.query.get(id)

      # Check if the movie exists in the database
      if movie is None:
          # If the actor doesn't exist, add a message into json with error (not found - 404)
          return json.dumps({
              'success': False,
              'error': 'Movie #' + id + ' not found to be edited'
              }), 404

      # Get the form's data from the request
      body = request.get_json()

      # Check if the json keys exist
      if ('title' not in body) and ('release-date' not in body):
          # If both keys are missing, send an error (unprocessable - 422)
          abort(422)

      # Check if both, the title and release date, are missing
      if (body['title'] is None) and (body['release-date'] is None):
          # If both fields are missing, send an error (unprocessable - 422)
          abort(422)

      # Check the user's updated fields and assign them to variables (if exists)
      if 'title' in body:
          title = body['title']
          # Assign the new title to the old movie's title
          movie.title = title
      if 'release-date' in body:
          release_date = body['release-date']
          # Assign the new release_date to the old movie's release_date
          movie.release_date = release_date

      try:
          # Update the movie's data
          movie.update()

          # Return a status code 200 and json of movie's details and set the success message to true
          return jsonify({
              'success': True,
              'movie': movie.format()
          }), 200

      except:
          # If an error occured while proccessing the UPDATE, send an error (unprocessable - 422)
          abort(422)

  # This endpoint UPDATES a specified actor
  @app.route('/actors/<int:id>', methods=['PATCH'])
  # Require the 'patch:actors' permission
  @requires_auth('patch:actors')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it
  def update_actor(payload, id):
      # Retrieve the specified actor from the database by its ID
      actor = Actor.query.get(id)

      # Check if the actor exists in the database
      if actor is None:
          # If the actor doesn't exist, add a message into json with error (not found - 404)
          return json.dumps({
              'success': False,
              'error': 'Actor #' + id + ' not found to be edited'
              }), 404

      # Get the form's data from the request
      body = request.get_json()

      # Check if the json keys exist
      if ('name' not in body) and ('age' not in body) and ('gender' not in body):
          # If both keys are missing, send an error (unprocessable - 422)
          abort(422)

      # Check if all, the name, age and gender, are missing
      if (body['name'] is None) and (body['age'] is None) and (body['gender'] is None):
          # If all fields are missing, send an error (unprocessable - 422)
          abort(422)

      # Check the user's updated fields and assign them to variables (if exists)
      if 'name' in body:
          name = body['name']
          # Assign the new name to the old actor's name
          actor.name = name
      if 'age' in body:
          age = body['age']
          # Assign the new age to the old actor's age
          actor.age = age
      if 'gender' in body:
          gender = body['gender']
          # Assign the new gender to the old actor's gender
          actor.gender = gender 

      try:
          # Update the actor's data
          actor.update()

          # Return a status code 200 and json of actor's details and set the success message to true
          return jsonify({
              'success': True,
              'actor': actor.format()
          }), 200

      except:
          # If an error occured while proccessing the UPDATE, send an error (unprocessable - 422)
          abort(422)

  # This endpoint DELETES a specified movie
  @app.route('/movies/<int:id>', methods=['DELETE'])
  # Require the 'delete:movies' permission
  @requires_auth('delete:movies')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it
  def delete_movie(payload, id):
      # Retrieve the specified movie from the database by its ID
      movie = Movie.query.get(id)
      # Check if the movie exists in the database
      if not movie:
          # If the movie doesn't exist, send an error (not found - 404)
          abort(404)
          """
          return json.dumps({
              'success': False,
              'error': 'Movie #' + id + ' not found to be deleted'
              }), 404
          """

      try:
          # Delete the movie from the database
          movie.delete()

          # Return a status code 200 and json of the movie's id and set the success message to true
          return jsonify({
              'success': True,
              # Return the deleted movie's id
              'deleted': id
          }), 200

      except:
          # If an error occured while proccessing the UPDATE, send an error (unprocessable - 422)
          abort(422)

  # This endpoint DELETES a specified actor
  @app.route('/actors/<int:id>', methods=['DELETE'])
  # Require the 'delete:actors' permission
  @requires_auth('delete:actors')
  # Because of calling the 'requires_auth', we need to take the payload as it returns it
  def delete_actor(payload, id):
      # Retrieve the specified actor from the database by its ID
      actor = Actor.query.get(id)
      # Check if the actor exists in the database
      if not actor:
          # If the actor doesn't exist, send an error (not found - 404)
          abort(404)
          """
          return json.dumps({
              'success': False,
              'error': 'Actor #' + id + ' not found to be deleted'
              }), 404
          """

      try:
          # Delete the actor from the database
          actor.delete()

          # Return a status code 200 and json of the actor's id and set the success message to true
          return jsonify({
              'success': True,
              # Return the deleted actor's id
              'deleted': id
          }), 200

      except:
          # If an error occured while proccessing the UPDATE, send an error (unprocessable - 422)
          abort(422)


  ## Error Handling
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": "Not Processable"
                      }), 422

  # Error Handler for (404 - Not Found)
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'Resource Not Found'
      }), 404

  # Error Handler for (400 - Bad Request)
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad Request'
      }), 400

  # Error Handler for (500 - Internal Server Error)
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal Server Error'
      }), 500

  # Error Handler for (405 - Method Not Allowed)
  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'Method Not Allowed'
      }), 405

  @app.errorhandler(AuthError)
  def auth_error(e):
      return jsonify({
          'success': False,
          'error': e.status_code,
          'message': e.error['description']
      }), e.status_code


  return app

app = create_app()

# Default port:
if __name__ == '__main__':
  app.debug = True
  app.run()
