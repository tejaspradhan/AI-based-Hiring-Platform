from pymongo import MongoClient

from flask import Flask, url_for, render_template, request
from werkzeug.utils import secure_filename
from Helper import Helper
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
import os
app = Flask(__name__)
helper = Helper()
client = MongoClient('localhost', 27017)
db=client.edi_hiring_db
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/employee")
def index():
    return render_template('employee-signup.html')

@app.route("/employer")
def index1():
    return render_template('employer-signup.html')


@app.route("/employee/login", methods=['GET', 'POST'])
def employee_login():
    print(request.form['username'])
    print(request.form['password'])
    return render_template('index.html')

@app.route("/employer/login", methods=['GET', 'POST'])
def employer_login():
    print(request.form['username'])
    print(request.form['password'])
    return render_template('index.html')

@app.route("/employer/signup", methods=['GET', 'POST'])
def employer_signup():
    print(request.form['username'])
    print(request.form['password'])
    empr_details={"name":request.form['username'],
    "email":request.form['email'],
    "number":request.form['cnum'],
    "password":request.form['password']}
    employer=db.employer
    empr_id=employer.insert_one(empr_details).inserted_id
    print(empr_id)
    return render_template('index.html')

@app.route("/employee/signup", methods=['GET', 'POST'])
def employee_signup():
    print(request.form)
    f = request.files['resume']
    f.save(secure_filename(f.filename))
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(
        resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(f.filename, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        pdfText = fake_file_handle.getvalue()
        pdfText = helper.cleanTextAndTokenize(pdfText)
    os.remove(secure_filename(f.filename))
    emp_details={"name":request.form['username'],
    "email":request.form['email'],
    "number":request.form['cnum'],
    "password":request.form['password'],
    "skills":pdfText}
    employee=db.employee
    emp_id=employee.insert_one(emp_details).inserted_id
    print(emp_id)
    return render_template('index.html', text=pdfText)


if __name__ == '__main__':
    app.run(debug=True)
