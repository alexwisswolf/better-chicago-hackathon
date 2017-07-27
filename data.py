from google.cloud import datastore
import json

gcp_project_id = "better-chicago-hackathon"
ds_client = datastore.Client(gcp_project_id)

def get_crimes():
    query = ds_client.query(kind="crime")    
    results = list(query.fetch())
    json_crimes = json.dumps(results)
    return json_crimes
