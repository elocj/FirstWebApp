import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False


db = SQLAlchemy(app)

class People(db.Model):
    name = db.Column(db.String(80), unique = True, nullable = False, primary_key = True)
    val = db.Column(db.String(80), unique = False, nullable = False, primary_key = False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

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

@app.route("/portfolio/update", methods=["POST", "GET"])
def update(): # you can pass name input and getname button from home page
    # name = request.form.get("nam")
    num = request.form.get("num")
    # person = People.query.filter_by(name=name).first()
    # db.session.delete(person)
    text = num
    # person.val = num
    db.session.commit()
    return redirect("/portfolio")

@app.route('/portfolio', methods=["POST", "GET"])
def portfolio():
    images = os.listdir('static')
    name = request.form.get("nam")
    person = People.query.filter_by(name=name).first()
    person.val = person.val + "jjjeje"
    db.session.commit()
    return render_template("prog.html", images=images, person=person, name=name)

@app.route("/delete", methods=["POST", "GET"])
def delete():
    name = request.form.get("name")
    # num = request.form.get("num")
    person = People.query.filter_by(name=name).first()
    db.session.delete(person)
    # person.val = person.val + num
    db.session.commit()
    return redirect("/")

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.form:
        try:
            people = People(name=request.form.get("name"), val = request.form.get("val"))
            db.session.add(people)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    peoples = People.query.all()
    return render_template("home.html", peoples=peoples)

if __name__ == "__main__":
    app.run(debug = True)