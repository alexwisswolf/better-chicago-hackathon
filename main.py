"""
Main code for the Better Chicago Hackathon webapp.
"""
from flask import (
    Flask
)
import data

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello!"

@app.route("/_crimes")
def _crimes():
    return data.get_crimes()

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)