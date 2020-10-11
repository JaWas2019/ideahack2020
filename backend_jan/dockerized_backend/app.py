import os
import numpy as np
from numpy.linalg import norm

import pandas as pd

from flask import Flask
from flask_restful import Api, Resource, reqparse

from operator import itemgetter

app = Flask(__name__)
api = Api(app)

employee_skill_matrix = pd.read_pickle("employeeskillmatrix.pkl")
relation_matrix = pd.read_pickle("relationmatrix.pkl")
occupation_codes = list(relation_matrix.index)
employee_names = list(employee_skill_matrix.index)


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

class Test(Resource):
    def get(self):
        return "This is working just fine!"

api.add_resource(Company_req, "/company/<string:occupation_uri>/<int:n>")
api.add_resource(Employee_req, "/employee/<string:employee_name>/<int:n>")
api.add_resource(Test, "/test")

if __name__=="__main__":
    app.run (debug=True, host="0.0.0.0")