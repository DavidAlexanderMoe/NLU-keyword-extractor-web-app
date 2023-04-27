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
from flask import Flask, request, render_template, redirect, session
from flask_login import LoginManager, login_user, logout_user, login_required
import requests

# with this the app can work also in other workstations
# make the url a parameter to define port
# ADD IT TO THE .ENV FILE IN TEMPLATES TO PROTECT THIS INFO
# TREAT THEM LIKE ENVIRONMENT VARIABLES
SEARCH_NLU_ENDPOINT = os.getenv("SEARCH_NLU_ENDPOINT")

# DO THE SAME WIHT THE TEST LOGIN CREDENTIALS
AUTHENTICATION_USERNAME = os.getenv("AUTH_USERNAME")
AUTHENTICATION_PASSWORD = os.getenv("AUTH_PASSWORD")

# CREATE FLASK SERVER
app = Flask("frontend-flask")

# Main page
@app.route("/", methods=["GET"])
# add decorator to protect the main page saying that the login is required
@login_required
# this works only if the user is logged in
# but if the user is not logged in we need to tell flask what is the next action
# basically redirect the user to the login page  -> create the una
def homepage():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])             # the /analyze should be the same as the one you put in the html <form>
@login_required
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

# use login_required to add a decorator to every part that need to be protected

# import user models from UserModel
from UserModel import User

tester = User()

# implement the login strategy inside my server
login_manager = LoginManager()
login_manager.init_app(app)

# setup a unique and not disclosed value for the secret of the session
app.secret_key = os.getenv("SESSION_SECRET")    # just some random characters

# tell flask how to retrieve the user
@login_manager.user_loader
def load_user(user_id):
    print("checking if user is logged in", user_id, tester.get_id())
    if tester.get_id() == user_id:
        print("user is logged in")
        return tester
    else:
        print("user is NOT logged in")
        return None

# tell flask what to do if a user that is NOT authenticated tries to access a protected page
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

# login page
@app.route("/login", methods=["GET"])
def loginpage():
    return render_template("login.html")

# setup route that collects the post requests from the frontend
@app.route("/login", methods=["POST"])
def login():
    # collect login parameters of the user
    form_username = request.form['username']
    form_password = request.form['password']

    print("user tried to login:", form_username, form_password)

    # check if the username and password are correct
    # we're not planning to save the credentials inot a DB, but we're going to check
    # if the username is the expected one i told the user
    
    
    if form_username == AUTHENTICATION_USERNAME and form_password==AUTHENTICATION_PASSWORD:
        # log in the user using my UserModel.py class
        print("username and password correct, logging in the user")
        session['username'] = form_username
        login_user(tester)
        # login_user() creates inside the internal DB of flask login the info that the user tester is acutally logging in
        # if we were working with a DB these 2 lines would change to find the user with these credentials and then retrieve those info from the DB and then tell flask login that that specific user has tried to login
        
        # redirect the user to the /main page
        return redirect("/")
    
    else:
        # user is not authorized
        print("username and password not correct")
        # redirect to the /login page
        return redirect("/login")


# loout page
@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    # telling flask to remove the user
    session.pop('username', None)     # remove and set username to None
    session['logged_in'] = False
    return redirect("/login")


####################################################
app.run(host='0.0.0.0', port=8080) # different port than app.py in order to let both run at same time
