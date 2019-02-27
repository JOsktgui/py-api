from flask import Flask, jsonify, request, Response, make_response
import json

app = Flask(__name__)

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
  return jsonify({ 'books': books })

# GET
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
  return_value = {}
  for book in books:
    if book['isbn'] == isbn:
      return_value = {
        'name': book['name'],
        'price': book['price'],
        'isbn': book['isbn']
      }

  return jsonify(return_value)

# POST
@app.route('/books', methods=['POST'])
def add_book():
  request_data = request.get_json()

  if (validBookObject(request_data)):
    new_book = {
      'name': request_data['name'],
      'price': request_data['price'],
      'isbn': request_data['isbn']
    }
    books.insert(0, new_book)
    response = Response('', 201, mimetype='application/json')
    response.headers['Location'] = '/books/' + str(new_book['isbn'])
    return response
  else:
    invalidBookObjectErrorMsg = {
      'error': 'Invalid book object passed in request',
      'helpString': 'Data passed in similar to this {"name": "bookname", "price", 4.88, "isbn": 232222}'
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status = 400, mimetype='application/json')
    return response


app.run(port = 5000)