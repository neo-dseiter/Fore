from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import matplotlib.pyplot as plt
from io import BytesIO

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

@app.route("/delete", methods=["POST"])
def delete_round():
    round_id = request.form.get("round_id")
    if round_id:
        # locate the round by id and delete it
        round_to_delete = GolfRound.query.get(int(round_id))
        if round_to_delete:
            db.session.delete(round_to_delete)
            db.session.commit()
        else:
            print(f"No round found with id {round_id}")
    return redirect(url_for("index"))

@app.route("/plot.png")
def plot_png():
    rounds = GolfRound.query.order_by(GolfRound.id).all()
    scores = [r.score for r in rounds]
    round_id = [r.id for r in rounds]

    fig, ax = plt.subplots()
    ax.plot(round_id, scores, marker='o')
    ax.set_title("Golf Scores Over Time")
    ax.set_xlabel("Round ID")
    ax.set_ylabel("Score")
    ax.grid(True)

    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return app.response_class(img.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create db tables if they don't exist already
    app.run(debug=True)
