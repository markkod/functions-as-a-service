import sys
import json
from cloudant.client import Cloudant

def add_registration(reg, username, apikey):
    database_name = "registration"
    client = Cloudant.iam(username, apikey, connect=True)
    database = client[database_name]
    return database.create_document(reg)
    

def main(param):
    first_name = param['first_name']
    last_name = param['last_name']
    email = param['email']
    registration = {'first_name': first_name, 'last_name': last_name, 'email': email}
    new_doc = add_registration(registration, param['username'], param['apikey'])
    return new_doc 
    