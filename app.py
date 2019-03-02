from flask import Flask, jsonify, request, Response
from BookModel import *
from settings import *
import json

books = [
  {
    'name': 'Green Eggs and Ham',
    'price': 5.99,
    'isbn': 213828182819102
  }, {
    'name': 'The Cat In The Hat',
    'price': 1.99,
    'isbn': 112131222122
  }
]

def validBookObject(bookObject):
  if ('name' in bookObject and 'price' in bookObject and 'isbn' in bookObject):
    return True
  else:
    return False

############# ROUTES #############
# GET
@app.route('/books')
def get_books():
  return jsonify({ 'books': Book.get_all_books() })

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
  return_value = Book.get_book(isbn)
  return jsonify(return_value)

# POST
@app.route('/books', methods=['POST'])
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
def replace_book(isbn):
  request_data = request.get_json()
  Book.replace_book(isbn, request_data['name'], request_data['price'])
  response = Response('', status=204)
  return response

# PATCH
@app.route('/books/<int:isbn>', methods=['PATCH'])
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
def delete_book(isbn):
  if (Book.delete_book(isbn)) {
    response = Response('', status=204)
    return response
  }
  
  invalidBookObjectErrorMsg = {
    'msg': 'Book with the ISBN number that was provided was not found!'
  }
  response = Response(json.dumps(invalidBookObjectErrorMsg), status=204, mimetype='application/json')
  return response

app.run(port = 5000)