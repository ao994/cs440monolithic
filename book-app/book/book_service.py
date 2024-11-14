from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages
REVIEW_SERVICE_URL = 'http://nginx:5000/reviews'

def init_db():
    connection = get_db_connection()
    with open('squema.sql', 'r') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    connection = get_db_connection()
    books = connection.execute('SELECT * FROM books').fetchall()
    connection.close()
    return render_template('books.html', books=books)

@app.route('/books/<int:book_id>')
def book_details(book_id):
    connection = get_db_connection()
    book = connection.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    connection.close()
    
    # Request reviews from the Review Microservice
    reviews = requests.get(f"{REVIEW_SERVICE_URL}/{book_id}/api").json()
    
    return render_template('reviews.html', book=book, reviews=reviews)


@app.route('/books/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    
    connection = get_db_connection()
    connection.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
                (title, author, year))
    connection.commit()
    connection.close()
    flash('Book added successfully!')
    return redirect(url_for('books'))

@app.route('/books/api')
def api_books():
    connection = get_db_connection()
    books = connection.execute('SELECT * FROM books').fetchall()
    connection.close()
    return jsonify([dict(book) for book in books])

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
