# FRONTEND FOR APP.PY:
# create frontend folder and all the modifications needed
# create html file and use render_twmplate to read it
# oper PS and go into frontend directory with cd frontend
# run the main file: see the url where it is running
# wee need to make it prettier and let the user be able to use it
# create a new route that manages the interaction with the html form
# use requests module to call api and get info on url
# open second terminal, cd search-nlu, python app.py, copy url at which is running
# insert the url in the .post request, add /search whcih is the endpoint

# after committing all the changes we can do many things like:
# push the app to kubernetes;
# or protect a little bit more our app -> people could use all our calls!
# setup a login page for our app, but we are not going to do this in a proper way
# (not using database) -> we'll simply use flask login
# use a /login endpoint to ask user/password and if authenticated
# (authentication part is crucial -> check if user is in database) flask puts a session token to recognize the user and
# i can decide which endpoints the user will have access to
# the simple login we'll use is by creating a new user, putting it into a database and then returning to the login page
# to login



# read and load environment variables
from dotenv import load_dotenv
load_dotenv()

# IMPORT DEPENDENCIES
import json, os
from flask import Flask, request, render_template
import requests

# with this the app can work also in other workstations
# make the url a parameter to define port
# ADD IT TO THE .ENV FILE IN TEMPLATES
SEARCH_NLU_ENDPOINT = os.getenv("SEARCH_NLU_ENDPOINT")

# CREATE FLASK SERVER
app = Flask("frontend-flask")

# Main page
@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])             # the /analyze should be the same as the one you put in the html <form>
def search():
    print("Received call to /search endpoint")
    # collecting parameters
    url_to_search = request.form["webpage"]          # read content of the request
    print("url to search:", url_to_search)
    # send request to nlu backend (search-nlu)
    payload = json.dumps({"url": url_to_search})
    headers = {'Content-type': 'application/json'}
    nlu_results_raw = requests.request("POST", SEARCH_NLU_ENDPOINT, headers=headers, data=payload)
    nlu_results = nlu_results_raw.json()
    print(nlu_results)
    # return results
    # for example: return "<h1>Results</h1><p>... SOME RESULTS ...</p>"
    results_page = "<h1>Results</h1>"
    results_page += "<p>Within the selected webpage I have extracted the following kewords:</p>"
    results_page += "<p>"                       # open the section
    for keyword in nlu_results['results:']:
        results_page += keyword + "</br>"       # add new line with breakpoint
    results_page += "</p>"                      # close the paragraph
    results_page += "<a href=\"/\">Return to homepage</a>"                  # add html link
    # by adding \/ you get that the "" are part of the string
    return results_page

# health check
@app.route("/health", methods=["GET"])
def health_check():
    return {"status:": "healthy", "code": 200}


####################################################
#################  LOGIN  ##########################

# flask login example (outdates)
# documentation: https://pythonbasics.org/flask-login/

# pip install flask-login
from Flask_login import LoginManager, login_user

# import user models from UserModel
from UserModel import User

login_manager = LoginManager()
login_manager.init_app(app)

# login page
@app.route("/login", methods=["GET"])
def loginpage():
    return render_template("login.html")


####################################################
app.run(host='0.0.0.0', port=8080) # different port than app.py in order to let both run at same time
