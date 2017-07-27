from google.appengine.ext import ndb
from flask import jsonify

gcp_project_id = "better-chicago-hackathon"
ds_client = datastore.Client(gcp_project_id)

def get_crimes():
    query = ds_client.query(kind=Crime)    
    results = list(query.fetch())
    return results
