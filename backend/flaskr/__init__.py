import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
remaining_questions = set()

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_all_categories():
    '''
      return all categories in json format
    '''
    selection = Category.query.order_by(Category.id).all()
    categories = [category.type for category in selection]

    if len(selection) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories,
      'total_categories': len(Category.query.all())
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    '''
      This endpoint should return a list of questions, 
      number of total questions, current category, categories.
      including pagination (every 10 questions).
    '''
    response = {
      'success': True
    }
    
    selection = Question.query.order_by(Question.id).all()
    response["current_category"] = "All"
    
    response["questions"] = paginate_questions(request, selection)
    response["total_questions"] = Question.query.count()

    selection = Category.query.order_by(Category.id).all()
    categories = [category.type for category in selection]
    response["categories"] = categories

    if len(response["questions"]) == 0:
      abort(404)

    return jsonify(response)

  @app.route('/categories/<category_id>/questions')
  def get_category_questions(category_id):
    '''
      This endpoint should return a list of questions of category <category_id>, 
      number of total questions, current category, categories.
      including pagination (every 10 questions).

      params:
      category_id (str): ID of the selected category 
    '''
    response = {
      'success': True
    }
    selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    category = Category.query.get(category_id)
    if category:
      response["current_category"] = category.type
    else:
      response["current_category"] = "All"

    response["questions"] = paginate_questions(request, selection)
    response["total_questions"] = Question.query.count()

    selection = Category.query.order_by(Category.id).all()
    categories = [category.type for category in selection]
    response["categories"] = categories

    if len(response["questions"]) == 0:
      abort(404)

    return jsonify(response)
    

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    '''
      This endpoint to DELETE question using a question ID.
    '''
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id,
        'total_questions': Question.query.count()
      })

    except Exception as ex:
      print(ex)
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    '''
      an endpoint to get questions based on a search term or 
      POST a new question, which will require the question and answer text, 
      category, and difficulty score.
    '''
    body = request.get_json()
      
    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)
    search = body.get('searchTerm', None)

    try:
      if search:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection.all())
          })
      
      else:
        question = Question(**body)
        question.insert()

        return jsonify({
          'success': True,
          'created': question.id,
          'total_questions': Question.query.count()
        })

    except:
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
  @app.route('/quizzes/<category_id>', methods=['POST'])
  def get_question(category_id=None):
    '''
      a POST endpoint to get questions to play the quiz. 
      This endpoint should take <category_id> as parameter 
      and previous question <prev_q> as query parameter 
      and return a random questions within the given category, 
      if provided, and that is not one of the previous questions.
    '''
    global remaining_questions
    
    prev_question_id = request.args.get('prev_q', None, type=int)
    if prev_question_id is None:
      if category_id is None:
        remaining_questions = set(Question.query.all())
      else:
        remaining_questions = set(Question.query.filter(Question.category == category_id).all())
    
    if len(remaining_questions):
      question = remaining_questions.pop()
      
      return jsonify({
        'success': True,
        'question': question.format(),
        'remaining_questions': len(remaining_questions)
        })
    
    else:
      return jsonify({
        'success': True,
        'done': True
        })



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  return app

    