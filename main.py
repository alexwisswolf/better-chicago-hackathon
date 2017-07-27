"""
Main code for the Better Chicago Hackathon webapp.
"""
from flask import (
    Flask,
    render_template,
    send_file
)
import data

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route("/")
def index():
    return render_template("map.html")

@app.route("/_crimes")
def _crimes():
    return data.get_crimes()

@app.route("/assets/cps_boundaries.kml")
def boundaries_kml():
    return send_file("assets/cps_boundaries.kml")

@app.route("/assets/line.kml")
def line():
    return send_file("assets/line.kml")

@app.route("/assets/cps_boundaries.json")
def boundaries_json():
    return send_file("assets/cps_boundaries.json")

@app.route("/assets/circles.json")
def circles():
    return send_file("assets/circles.json")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)