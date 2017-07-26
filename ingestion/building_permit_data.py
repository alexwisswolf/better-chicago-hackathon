from google.cloud import datastore
import requests
import json

gcp_project_id = "better-chicago-hackathon"
ds_client = datastore.Client(gcp_project_id)

response = requests.get("https://data.cityofchicago.org/resource/building-permits.json")

permit_data = json.loads(response.text)
for permit in permit_data:
    ds_permit = datastore.Entity(ds_client.key('permit', permit['id']))
    for key, val in permit.iteritems():
        if type(val) is dict:
            ds_permit[key] = datastore.Entity(ds_client.key(key))
            for nest_key, nest_val in val.iteritems():
                ds_permit[key][nest_key] = nest_val
        else:
            ds_permit.update({key: val})
    
    ds_client.put(ds_permit)