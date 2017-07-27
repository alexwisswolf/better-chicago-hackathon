"""
Main code for the Better Chicago Hackathon webapp.
"""
from flask import (
    Flask,
    render_template
)
import data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/_crimes")
def _crimes():
    return data.get_crimes()



if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)