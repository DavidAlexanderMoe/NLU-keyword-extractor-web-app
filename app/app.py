# READ ENVIRONMENT VARIABLES
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# IMPORT DEPENDENCIES
import json, os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
from flask import Flask, request

# getenv() -> read the value of the environment variable
NLU_BASEURL = os.getenv("NLU_BASEURL")
NLU_VERSION = os.getenv("NLU_VERSION")
NLU_APIKEY = os.getenv("NLU_APIKEY")


# AUTHENTICATE WITH THE SERVICE
authenticator = IAMAuthenticator(NLU_APIKEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version=NLU_VERSION,
    authenticator=authenticator
)
natural_language_understanding.set_service_url(NLU_BASEURL)


# FUNCTION TO PERFORM ANALYZE QUERY ON NLU
def nlu_search(url_to_query):
    out = []
    response = natural_language_understanding.analyze(
        url=url_to_query,
        features=Features(
            keywords=KeywordsOptions(limit=10)
        )
    ).get_result()
    # print(json.dumps(response, indent=2, ensure_ascii=False))

    print("Webpage searched:",url_to_query)
    print("KEYWORDS extracted:")

    for keyword in response["keywords"]:
        out.append(keyword["text"])
        print(keyword["text"])

    return out


# CREATE FLASK SERVER
app = Flask("nlu-search-flask")

# Main page
@app.route("/search", methods=["POST"])                 # /search is the endpoint
def start_search():
    print('Received request to search on NLU')
    print('request json:', request.json)
    url = request.json['url']
    keywords = nlu_search(url)
    return {"input:":url, "results:":keywords}

@app.route("/health", methods=["GET"])
def health_check():
    return {"status:": "healthy", "code": 200}

app.run(host='0.0.0.0', port=3000)
