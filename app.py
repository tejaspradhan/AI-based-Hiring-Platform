from pymongo import MongoClient
from flask import Flask, url_for, render_template, request, session
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from Helpers.Helper import Helper
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
import os
app = Flask(__name__)
bcrypt = Bcrypt(app)
helper = Helper()
client = MongoClient('localhost', 27017)
db = client.edi_hiring_db
emid = ''
app.config['SECRET_KEY'] = '14ec258c169f5c19f78385bcc83a51df7444624b2ff90449b4a9832e6fe706a1'

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/employee")
def index():
    return render_template('employee-signup.html')


@app.route("/employer")
def index1():
    print("hi")
    return render_template('employer-signup.html')


@app.route("/employee/login", methods=['GET', 'POST'])
def employee_login():
    global emid
    print(request.form['email'])
    print(request.form['password'])
    employee_cred = db.employee.find_one({'email': request.form['email']}, {
                                         'email': 1, 'password': 1})
    if(not bool(employee_cred)):
        return render_template('employee-signup.html')
    if(bcrypt.check_password_hash(employee_cred['password'], request.form['password'])):
        emid = employee_cred['_id']
        proj = db.projects.find()
        return render_template('employee-dashboard.html', alljobs=proj)
    else:
        return render_template('employee-signup.html')


@app.route("/employer/login", methods=['GET', 'POST'])
def employer_login():
    print(request.form['email'])
    print(request.form['password'])
    employer_cred = db.employer.find_one({'email': request.form['email']}, {
        'email': 1, 'password': 1})
    if(not bool(employer_cred)):
        return render_template('employer-signup.html')
    if(bcrypt.check_password_hash(employer_cred['password'], request.form['password'])):
        session['empemail'] = employer_cred['email']
        job = db.projects.find({'email': session['empemail']})
        print("hello",job)
        return render_template('employer-dashboard.html', jobs=job)
    else:
        return render_template('employer-signup.html')


@app.route("/employer/signup", methods=['GET', 'POST'])
def employer_signup():
    print(request.form['name'])
    print(request.form['password'])
    password_hash = bcrypt.generate_password_hash(request.form['password'], 10)
    empr_details = {"name": request.form['name'],
                    "email": request.form['email'],
                    "number": request.form['cnum'],
                    "password": password_hash}
    empr_id = db.employer.insert_one(empr_details).inserted_id
    print(empr_id)
    return render_template('employer-login.html')


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
    password_hash = bcrypt.generate_password_hash(request.form['password'], 10)
    emp_details = {"name": request.form['name'],
                   "email": request.form['email'],
                   "number": request.form['cnum'],
                   "password": password_hash,
                   "skills": pdfText}
    emp_id = db.employee.insert_one(emp_details).inserted_id
    print(emp_id)
    return render_template('employee-login.html')

@app.route("/employer/addJobs", methods=['POST'])
def add_jobs():
    proj_title = request.form['title']
    proj_skills = request.form['skills']
    print("Session email",session['empemail'])
    job_details = {
                    "email": session['empemail'],
                    "title": proj_title,
                    "skills": proj_skills,
                    "appliedemp": []
                    }
    empr_id = db.projects.insert_one(job_details).inserted_id
    print(empr_id)
    jobs=db.projects.find({"email":session['empemail']})
    return render_template('employer-dashboard.html',jobs=jobs)

@app.route("/employee/apply/<project_id>", methods=["GET", "POST"])
def apply_project(project_id):
    print(project_id)
    global emid
    """db.projects.update(
           { _id: project_id },
           { $push: {appliedemp : emid } }
       )"""
    return render_template("employee-dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)
