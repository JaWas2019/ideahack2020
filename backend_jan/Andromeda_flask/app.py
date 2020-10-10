"""
ENJOY THE FUCKING SPAGHETTI LOL
- JAN
"""

import os
import pandas as pd
import numpy as np
import asyncio
import aiohttp
from contextlib import closing
from numpy.linalg import norm
from operator import itemgetter
from flask import Flask
from flask_restful import Api, Resource, reqparse
from azure.storage.blob.aio import BlobClient, BlobServiceClient
from connection import connection_string

async def download_blob(filename, containername):
    # Instantiate a new BlobServiceClient using a connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    async with blob_service_client:
        container_client = blob_service_client.get_container_client(containername)
        try:
            # Instantiate a new BlobClient
            blob_client = container_client.get_blob_client(filename)
            with open(filename, "wb") as my_blob:
                stream = await blob_client.download_blob()
                data = await stream.readall()
                my_blob.write(data)
        finally:
            print("Yeehaw!")

async def main():
    global employee_skill_matrix
    global relation_matrix
    global occupation_codes
    global employee_names

    await download_blob("employeeskillmatrix.pkl", "pickelbarrel")
    await download_blob("relationmatrix.pkl", "pickelbarrel")

    employee_skill_matrix = pd.read_pickle("employeeskillmatrix.pkl")
    relation_matrix = pd.read_pickle("relationmatrix.pkl")
    occupation_codes = list(relation_matrix.index)
    employee_names = list(employee_skill_matrix.index)

# creating own FlaskApp to run automated downloads on launch
class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = MyFlaskApp (__name__)
api = Api(app)

def cosine_sim_calculator (a, b):
    cos_sim = np.inner(a, b) / (norm(a) * norm(b))
    return cos_sim

def occupation_recommender_scores(user):
    employee_vector = np.array(employee_skill_matrix.loc[user])
    similarities = cosine_sim_calculator(np.atleast_2d(employee_vector), relation_matrix)
    return similarities[0]

def employee_recommender_scores(occupation_uri):
    occupation_vector = np.array(relation_matrix.loc[occupation_uri])
    similarities = cosine_sim_calculator(np.atleast_2d(occupation_vector), employee_skill_matrix)
    return similarities[0]

def occupation_recommender(user, n):
    result = occupation_recommender_scores(user)

    labeled_result = list(zip(occupation_codes, result))
    labeled_result.sort(key=itemgetter(1), reverse=True)
    return labeled_result[:n]

def employee_recommender(occupation_uri, n):
    result = employee_recommender_scores(occupation_uri)

    labeled_result = list(zip(employee_names, result))
    labeled_result.sort(key=itemgetter(1), reverse=True)
    return labeled_result[:n]

class Company_req(Resource):
    def get(self, occupation_uri, n):
        result = employee_recommender(occupation_uri, n)
        return result, 200

class Employee_req(Resource):
    def get(self, employee_name, n):
        result = occupation_recommender(employee_name, n)
        return result, 200

api.add_resource(Company_req, "/company/<string:occupation_uri>/<int:n>")
api.add_resource(Employee_req, "/employee/<string:employee_name>/<int:n>")

#if __name__=="__main__":
#    app.run(debug=True)