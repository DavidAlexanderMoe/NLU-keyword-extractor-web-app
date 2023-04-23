# we want to deploy this app in the cloud using kubernetes
# this app is already capable of running within a container and within a container orchestrations


# python app.py to run this
# open postman, put url in postman  http://127.0.0.1:3000/search with search be the endpoint
# send request and obtain results
# use postman to simulate the request and then take the python - request code to have the correct output
# </> code section to find it (topright in postman)

# now go to ibm.cloud and create a free tier kubernetes (catalog -> kubernetes service -> create)
# while the kubernetes is creating, open dockerhub, search python, select a desired version, copy it to the docker file (3.10-slim)
# terminal:
# docker
# ls
# docker build -t search-nlu:0.1 .                build image tag nome a caso:version a caso .
# docker images
# docker run -p 3000:3000 search-nlu:0.1
# (to stop it use ctrl + c or open new shell -> docker ps -> docker stop container_id)
# (to remove it use: docker rmi container_id -> and then you remove the image: docker images -> docker rmi image_id)
# send again request on postman
# stop with ctrl c
# docker ps -a to see which containers are active (rm to remove selecting the id)
# when sharing a docker image it is needed to exclude some files -> create a new file .dockerignore in which you will list all the files that
# you want to skip when building the image
# just write the folder to exclude
# *.pdf is to exclude all the pdf files
# private-* is to exclude all "private-"... files

# eliminate all existing containers
# create and run the container -> see that the run command needs to be more complex
# docker run -p 3000:3000 -e NAME_VAR=value_variable -e NAME_VAR=value_variable ... search-nlu:1.0
# and put in there the var and values in the .env file

# an alternative to the really long run command above is:
# docker run -p 3000:3000 --env-file .env search-nlu:1.0

# docker run -p 3000:3000 -e NLU_BASEURL=https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/47a3cf3a-4b24-413e-b480-3abe76a8eb67 -e NLU_VERSION=2022-04-07 -e NLU_APIKEY=RxYjDRyTHyjtsLu2FOPP5mZAol37eOmFeVcDW4PMWWRP search-nlu:1.0

# the app is composed by code + configuration file

# connection to the kubernetes: -> follow guide on blackboard
# ibmcloud login
# ibmcloud target -g Default
# ibmcloud ks clusters
# ibmcloud ks cluster config -c cge646if094ca58r9jjg (id or name its the same thing)
# verify that the kubernetes is activated: kubectl get nodes
# now start issuing command on the kubernetes itself: (kubectl)
# kubectl get namespaces
# we get a series of projects that are part of kubernetes
# go on cloud.ibm and open the kubernetes dashboard and see the same namespaces found with the above command
# the aim is to take the image from docker and import in the kubernetes: create a namespace in ibm.cloud
# install the proper plugin: ibmcloud plugin install container-service and rerun the command above
# ibmcloud plugin install container-registry -r 'IBM Cloud'
# ibmcloud cr region-set eu-central
# accessing container registry:
# docker login -u iamapikey -p BVxp0pzNEgBMkUi0kewNuwRmgbJbb4gyBZxLRmo4yvdZ de.icr.io
# tag and push the image:
# docker images
# docker tag search-nlu:1.0 de.icr.io/cloud-lab-david/search-nlu:1.0
# docker images
# docker push de.icr.io/cloud-lab-david/search-nlu:1.0
# now the image is imported into the container registry -> now the kubernetes can access it
# now we want to setup the configuration for deploying the app on kubernetes:
# (first pack of slides)
# kubectl create configmap search-nlu-configmap --from-literal="NLU_BASEURL=https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/47a3cf3a-4b24-413e-b480-3abe76a8eb67" --from-literal="NLU_VERSION=2022-04-07" 
# kubectl get configmaps
# now do the same thing with the secrets:
# kubectl create secret generic search-nlu-secret --from-literal="NLU_APIKEY=RxYjDRyTHyjtsLu2FOPP5mZAol37eOmFeVcDW4PMWWRP"
# kubectl get secrets

# Ready for the deployment:
# open kubernetes folder and modify the deployment.yaml file according to the name of the files i have
# kubectl apply -f kubernetes\deployment.yaml


# change app and upload new version
# docker build -t search-nlu:1.1 .
# docker run -p 3000:3000 --env-file .env search-nlu:1.1
# clean if neede the executed containers
# login to ibm with registry command
# ibmcloud login -a https://cloud.ibm.com
# ibmcloud target -g Default
# ibmcloud cr login
# tag this image locally and push it to container reg:
# docker tag search-nlu:1.1 de.icr.io/cloud-lab-david/search-nlu:1.1
# docker push de.icr.io/cloud-lab-david/search-nlu:1.1
# (if problems) docker login -u iamapikey -p BVxp0pzNEgBMkUi0kewNuwRmgbJbb4gyBZxLRmo4yvdZ de.icr.io
# change in deployment file from 1.0 to 1.1 (new file)
# setup the control for kubernetes to make: 
# add livenessprobe to deployment file at bottom (same level of env indentation)
# apply changes to the cluster:
# login to cluster:
# ibmcloud ks cluster config --cluster cge646if094ca58r9jjg
# apply new configuration to cluster:
# kubectl apply -f deployment.yaml (apply or delete)
# kubectl get pods
# the container is running but we need to define a service to let the user use it:
# create service.yaml
# kubectl apply -f service.yaml
# kubectl get services
# mapping to the port of the worker node (30232)
# i get an internal service + a NodePort service created by us with info about the ports (from 3000 to 30232/TCP port)
# this is one part of the public address which is necessary to access the app 

# PORT OF THE WORKER NODE TO WHICH MY SERVICE IS MAPPED: 30232
# IP PUBLIC ADDRESS OF THE WORKER NODE: ????

# LOCAL_IP_MAPPED: PORT_MAPPED/search
# 127.0.0.1:300/search

# IP_PUBLIC_WORKER:PORT_MAPPED/search
# x.x.x.x:30232/search

# several ways to retrieve the x.x.x.x:
# copy public ip from worker node form kubernetes dashboard
# 159.122.179.248:30232/search

# or

# kubectl get nodes -o wide
# and take the external IP
# 159.122.179.248 

# copy URL 159.122.179.248:30232/search on postman -> POST -> SEND -> SAME RESULTS AS WITH MY PERSONAL HTTP URL
# until now i tested everything locally -> with this url the testing is beign executed on the cloud
# everybody with this link can access our app and this is not good in some sense
# we are going to tranform this to an internal service for the public
# create a new microservice (webapp) to interact with it via browser 
# public will be able to issue the commands of our app

# we will modify the service to make it a clusterIP, modify service file to ClusterIP
# kubectl apply -f service.yaml
# kubectl get services



# CREATE FRONTEND FOR APPLICATION:
# setup a simple web app to allow user interaction



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
