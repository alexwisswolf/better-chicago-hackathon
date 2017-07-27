from google.cloud import datastore
import json


gcp_project_id = "better-chicago-hackathon"
ds_client = datastore.Client(gcp_project_id)

def get_crimes():
    query = ds_client.query(kind="crime")    
    results = list(query.fetch())
    for result in results:
        try:
            result['lat'] = result['latitude']
        except KeyError:
            result['lat'] = 0
        try:
            result['lng'] = result['longitude']
        except KeyError:
            result['lng'] = 0

    json_crimes = json.dumps(results)
    return json_crimes
