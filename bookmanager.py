import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from sqlalchemy.dialects import postgresql

from flask_sqlalchemy import SQLAlchemy

# def get_env_variable(name):
#     try:
#         return os.environ[name]
#     except KeyError:
#         message = "Expected environment variable '{}' not set.".format(name)
#         raise Exception(message)
#
# POSTGRES_URL = get_env_variable("POSTGRES_URL")
# POSTGRES_USER = get_env_variable("POSTGRES_USER")
# POSTGRES_PW = get_env_variable("POSTGRES_PW")
# POSTGRES_DB = get_env_variable("POSTGRES_DB")

# POSTGRES_URL="127.0.0.1:5000"
# POSTGRES_USER="postgres"
# POSTGRES_PW="dbpw"
# POSTGRES_DB="test"

# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

database_file = 'postgresql+psycopg2://login:pass@localhost/flask_app'

#
# from sqlalchemy import create_engine
#
# engine = create_engine(database_file)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)

class People(db.Model):
    name = db.Column(db.String(80), unique = True, nullable = False, primary_key = True)
    val = db.Column(db.String(80), unique = False, nullable = True, primary_key = False)
    # num = db.Column(postgresql.ARRAY(db.Integer), unique = False, nullable = True, primary_key = False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


# hoe as mother eduf
# db.create_all()
# db.session.commit()

# @app.route("/update", methods=["POST"])
# def update():
#     try:
#         newtitle = request.form.get("newtitle")
#         oldtitle = request.form.get("oldtitle")
#         book = Book.query.filter_by(title=oldtitle).first()
#         book.title = newtitle
#         db.session.commit()
#     except Exception as e:
#         print("Couldn't update book title")
#         print(e)
#     return redirect("/")
#
# @app.route("/delete", methods=["POST"])
# def delete():
#     title = request.form.get("title")
#     book = Book.query.filter_by(title=title).first()
#     db.session.delete(book)
#     db.session.commit()
#     return redirect("/")

@app.route('/portfolio')
def portfolio():
    images = os.listdir('static')
    return render_template("prog.html", images=images)

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.form:
        try:
            people = People(name=request.form.get("name"), val = request.form.get("val"), num = [1, 2, 3])
            db.session.add(people)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    images = os.listdir('static')
    peoples = People.query.all()
    return render_template("home.html", peoples=peoples)

if __name__ == "__main__":
    app.run(debug = True)