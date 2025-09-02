from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

golf_rounds = []

@app.route("/")
def index():
    return render_template("index.html", rounds=golf_rounds)

@app.route("/add", methods=["POST"])
def add_round():
    score = request.form.get("score")
    course = request.form.get("course")
    if score and course:
        golf_rounds.append({"course": course, "score": score})

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)