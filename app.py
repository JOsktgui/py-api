from flask import Flask, jsonify

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

# GET /books
@app.route('/books')
def get_books():
  return jsonify({ 'books': books })

# GET /books/<int:isbn>
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

app.run(port = 5000)