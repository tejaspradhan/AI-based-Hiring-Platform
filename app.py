# from pymongo import MongoClient

from flask import Flask, url_for, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

# client = MongoClient('localhost', 27017)


@app.route("/")
def index():
    return render_template('employee-signup.html')


@app.route("/employee/login", methods=['GET', 'POST'])
def employee_login():
    print(request.form['username'])
    print(request.form['password'])
    return render_template('index.html')


@app.route("/employee/signup", methods=['GET', 'POST'])
def employee_signup():
    print(request.form)
    f = request.files['resume']
    f.save(secure_filename(f.filename))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
