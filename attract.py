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
x = "global"

db = SQLAlchemy(app)

class People(db.Model):
    name = db.Column(db.String(80), unique = True, nullable = False, primary_key = True)
    val = db.Column(db.String(80), unique = False, nullable = False, primary_key = False)

    def __repr__(self):
        return "<Name: {}>".format(self.name)

@app.route("/portfolio/update", methods=["POST", "GET"])
def update():
    if request.form:
        try:
            global x
            x = request.form.get("name")
        except Exception as e:
            print("cant", e)
    return redirect("/portfolio")

# Final: Big issue was sending multiple requests to one page because it only took the first request
#        because second request had not been filled in yet
# Solution: Split into two routes but issue was I need way to send name to second route
#           so I used global variable (poor style)

@app.route("/portfolio/hoe", methods=["POST", "GET"])
def hoe():
    if request.form:
        try:
            num = request.form.get("num")
            num = str(num)
            person = get_peep(x)
            person.val = person.val + num
            db.session.commit()
        except Exception as e:
            print("cant", e)
    return redirect("/portfolio")

def get_peep(name):
    return People.query.filter_by(name=name).first()

@app.route('/portfolio', methods=["POST", "GET"])
def portfolio():
    images = os.listdir('static')
    return render_template("prog.html", images=images)

@app.route("/delete", methods=["POST", "GET"])
def delete():
    name = request.form.get("name")
    person = People.query.filter_by(name=name).first()
    db.session.delete(person)
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
    app.run(debug = True, threaded=True)