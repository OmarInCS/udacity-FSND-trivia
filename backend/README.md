# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

# on windows powershell
$FLASK_APP="flaskr"
$FLASK_ENV="development"
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints
- GET '/categories'
- GET '/questions'
- GET '/categories/<category_id>/questions'
- POST '/questions'
- POST '/quizzes'
- POST '/quizzes/<category_id>'
- DELETE '/questions/<<int:question_id>>'

> GET '/categories'
```
- Fetches a list of categories
- Request Arguments: None
- Returns: A a JSON object like:
{
    'success': True, 
    'categories': {
        "1":"Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    },
    'total_categories': 6
}
```

> GET '/questions'
```
- Fetches a list of all questions
- Request Arguments: None
- Returns: A a JSON object like:
{
    'success': True,
    'current_category': 'All',
    'questions': [
        {
            'id': 1,
            'question': 'who?',
            'answer': 'Omar',
            'category': 4,
            'difficulty': 1
        },
        ...
    ],
    'total_questions': 2,
    'categories': ["Science", "Art", "Geography", "History", "Entertainment", "Sports"]
}
```

> GET '/categories/<category_id>/questions'
```
- Fetches a list of questions of a specific category
- Request Arguments: category_id (str)
- Returns: A a JSON object like:
{
    'success': True,
    'current_category': 'All',
    'questions': [
        {
            'id': 1,
            'question': 'who?',
            'answer': 'Omar',
            'category': 4,
            'difficulty': 1
        },
        ...
    ],
    'total_questions': 2,
    'categories': ["Science", "Art", "Geography", "History", "Entertainment", "Sports"]
}
```

> POST '/questions'
```
- get questions include a searching term or create a new question
- Request Arguments: None
- Request Body: {
            'question': 'who?',
            'answer': 'Omar',
            'category': 4,
            'difficulty': 1
        }
        or
        {'searchTerm': 'movie'}
- Returns: A a JSON object like:
    {
        'success': True,
        'created': 15,
        'total_questions': 15
    }
    Or
    {
        'success': True,
        'questions': [{
            'id': 1,
            'question': 'who?',
            'answer': 'Omar',
            'category': 4,
            'difficulty': 1
        }, ...],
        'total_questions': 15
    }
```
> POST '/quizzes'

> POST '/quizzes/<category_id>'
```
- Fetches a questions, which can be of a specific category
- Request Arguments: optional category_id (str)
- Request Body: A a JSON object like:
    {
        "previous_questions": [2, 4]
    }
- Returns: A a JSON object like:
    if still question:
    {
        'success': True,
        'question': {
            'id': 1,
            'question': 'who?',
            'answer': 'Omar',
            'category': 4,
            'difficulty': 1
        }
    }
    Or if done:
    {
        'success': True,
        'done': True
    }
```

> DELETE '/questions/<<int:question_id>>'
```
- Delete the question with the specified question ID
- Request Arguments: question_id (int)
- Returns: {
        'success': True,
        'deleted': 2,
        'total_questions': 14
    }
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```