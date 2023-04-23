# FRONTEND FOR APP.PY:
# create frontend folder and all the modifications needed
# create html file and use render_twmplate to read it
# oper PS and go into frontend directory with cd frontend
# run the main file: see the url where it is running
# wee need to make it prettier and let the user be able to use it



# read and load environment variables
from dotenv import load_dotenv
load_dotenv()

# IMPORT DEPENDENCIES
import json, os
from flask import Flask, request, render_template

# CREATE FLASK SERVER
app = Flask("frontend-flask")

# Main page
@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

# health check
@app.route("/health", methods=["GET"])
def health_check():
    return {"status:": "healthy", "code": 200}

app.run(host='0.0.0.0', port=8080) # different port than app.py in order to let both run at same time
