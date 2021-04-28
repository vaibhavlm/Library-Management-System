# importing Flask and other modules
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import book_recommender

# Flask constructor
app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates'
            )
CORS(app)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')


@app.route('/book', methods=["POST"])
def process():
    if request.method == "POST":
        book_selected = request.form.getlist('book-choice')
        ratings = request.form.getlist('book-rating')
        # print(book_selected)
        # print(ratings)
        user_data = (book_selected, ratings)
        res = book_recommender.main(user_data)
        return jsonify(res)


if __name__ == '__main__':
    app.run()
