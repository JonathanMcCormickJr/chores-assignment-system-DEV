from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/survey")
def survey():
    return render_template("survey.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)

