from flask import Flask, jsonify, request, Response
from settings import *
from BookModel import *
from UserModel import User
from functools import wraps

import json
import jwt, datetime

app.config['SECRET_KEY'] = 'meow'

def validBookObject(bookObject):
  if ('name' in bookObject and 'price' in bookObject and 'isbn' in bookObject):
    return True
  else:
    return False


def token_required(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    token = request.args.get('token')
    try:
      jwt.decode(token, app.config['SECRET_KEY'])
      return f(*args, *kwargs)
    except:
      return jsonify({ 'error': 'Need a valid token to view this page' }), 401
  return wrapper

############# ROUTES #############
# GET
@app.route('/books')
@token_required
def get_books():
  return jsonify({ 'books': Book.get_all_books() })

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
  return_value = Book.get_book(isbn)
  return jsonify(return_value)

# POST
@app.route('/login', methods=['POST'])
def get_token():
  request_data = request.get_json()
  username = str(request_data['username'])
  password = str(request_data['password'])

  match = User.username_password_match(username, password)

  if match:
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({'exp': expiration_date }, app.config['SECRET_KEY'], algorithm='HS256')
    return token
  else:
    return Response('', 401, mimetype='application/json')

@app.route('/books', methods=['POST'])
@token_required
def add_book():
  request_data = request.get_json()

  if (validBookObject(request_data)):
    Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
    response = Response('', 201, mimetype='application/json')
    response.headers['Location'] = '/books/' + str(request_data['isbn'])
    return response
  else:
    invalidBookObjectErrorMsg = {
      'error': 'Invalid book object passed in request',
      'helpString': 'Data passed in similar to this {"name": "bookname", "price", 4.88, "isbn": 232222}'
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
    return response

# PUT
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
  request_data = request.get_json()
  Book.replace_book(isbn, request_data['name'], request_data['price'])
  response = Response('', status=204)
  return response

# PATCH
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
  request_data = request.get_json()

  if ('name' in request_data):
    Book.update_book_name(isbn, request_data['name'])

  if ('price' in request_data):
    Book.update_book_price(isbn, request_data['price'])
  
  response = Response('', status=204)
  response.headers['Location'] = '/books/' + str(isbn)
  return response

# DELETE
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
  if (Book.delete_book(isbn)):
    response = Response('', status=204)
    return response
  
  invalidBookObjectErrorMsg = {
    'msg': 'Book with the ISBN number that was provided was not found!'
  }
  response = Response(json.dumps(invalidBookObjectErrorMsg), status=204, mimetype='application/json')
  return response

app.run(port = 5000)