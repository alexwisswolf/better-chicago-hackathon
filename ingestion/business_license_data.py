from google.cloud import datastore
import requests
import json

gcp_project_id = "better-chicago-hackathon"
ds_client = datastore.Client(gcp_project_id)

response = requests.get("https://data.cityofchicago.org/resource/xqx5-8hwx.json")

license_data = json.loads(response.text)
for license in license_data:
    with ds_client.transaction():
        ds_license = datastore.Entity(ds_client.key('license', license['id']))
        for key, val in license.iteritems():
            ds_license.update({key: val})
        
        ds_client.put(ds_license)