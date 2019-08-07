import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from convoNN.cnn import Action
from convoNN.convTest import Test
import numpy as np
from werkzeug import secure_filename

from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "peopledatabase.db"))
UPLOAD_FOLDER = '/Users/anthonyjoo/Google Drive/Python/FirstWebApp/static/uploadImages'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
x = "global"

db = SQLAlchemy(app)

class People(db.Model):
    name = db.Column(db.String(80), unique = True, nullable = False, primary_key = True)
    val = db.Column(db.String(80), unique = False, nullable = True, primary_key = False)
    weights = db.Column(db.String(80), unique = False, nullable = True, primary_key = False)
    perc = db.Column(db.String(80), unique = False, nullable = True, primary_key = False)

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
    images = []
    for file in os.listdir('static/images'):
        images.append(os.path.join('static/images', file))
    return render_template("prog.html", images=images)


# run GETs a name and then queries that person and send it in through person=person and
# in the html it will get person.val and run the program. Results appended to person attr.
# in the future add a column for the weights and percentage swiped right
# action html should have the result details such as percentage and shit

# GET will receive the name to query and get the value which will then be sent through a python
# program where it will spit out your weights which you then post to action
@app.route("/run", methods = ["GET", "POST"])
def run():
    person = None
    num = None
    if request.form:
        try:
            name = request.form.get("name")
            person = get_peep(name)
            num = list(person.val)
            num = list(map(int, num))
            person.perc = getPerc(num) / 597
            person.weights = turnToString(runConv(num))
            db.session.commit()
        except Exception as e:
            print("something wrong")
            print(e)
    return render_template("action.html", person=person) # can change this to return redirect

def runConv(num):
    return Action(num).run()

def getPerc(num):
    return np.count_nonzero(num == 1)

def turnToString(arr):
    j = 2
    collect = str(arr[0][0]) + ', ' + str(arr[0][1])
    for i in range(1, 17672):
        collect += ', ' + str(arr[i][0]) + ', ' + str(arr[i][1])
        j += 2
    print(j, "hehrhehrehheWTFFFF")
    return collect

# For inputting your own pictures to rate yourself
@app.route("/rate", methods = ["GET", "POST"])
def rate():
    person = None
    text = None
    if request.form:
        try:
            name = request.form.get("name")
            person = People.query.filter_by(name=name).first()
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            arr = turnToArr(person.weights)
            arr = np.array(arr)
            arr = arr.astype(np.float)
            ans = testFace(filename, arr)

            if ans == 1:
                text = 'you like'
            else:
                text = 'you do not like'
        except Exception as e:
            print("something wrong")
            print(e)
    return render_template("rate.html", person=person, text = text)

def testFace(filename, weights):
    return Test(filename, weights).testIt()

def turnToArr(text):
    arr = text.split(', ')
    newarr = []
    i = 0
    while i < 35344:
        newarr.append([arr[i], arr[i + 1]])
        i += 2
    return newarr

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
            print("Failed to add people")
            print(e)
    peoples = People.query.all()
    return render_template("home.html", peoples=peoples)

if __name__ == "__main__":
    app.run(debug = True)