from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///golf.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# database model
class GolfRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Round {self.course} - {self.score}>"


@app.route("/")
def index():
    rounds = GolfRound.query.all()
    return render_template("index.html", rounds=rounds)


@app.route("/add", methods=["POST"])
def add_round():
    score = request.form.get("score")
    course = request.form.get("course")
    if score and course:
        new_round = GolfRound(course=course, score=int(score))
        db.session.add(new_round)
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create db tables if they don't exist already
    app.run(debug=True)
