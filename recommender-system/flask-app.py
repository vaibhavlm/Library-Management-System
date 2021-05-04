# importing Flask and other modules

from flask import Flask, request, render_template, jsonify
from flask_table import Table, Col
from flask_cors import CORS
import book_recommender

# Flask constructor
app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates'
            )
CORS(app)


# Declare the table
class ItemTable(Table):
    authors = Col('Authors')
    title = Col('Book Title')
    classes = ['table table-hover table-bordered ']


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')


@app.route('/result', methods=["POST"])
def process():
    if request.method == "POST":
        book_selected = request.form.getlist('book-choice')
        ratings = request.form.getlist('book-rating')
        user_data = (book_selected, ratings)
        items = book_recommender.main(user_data)
        table = ItemTable(items)
        return render_template('output.html', table=table)


if __name__ == '__main__':
    app.run(debug=True)
