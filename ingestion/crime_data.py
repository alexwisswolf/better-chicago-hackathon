from google.cloud import datastore
import requests
import json

gcp_project_id = "better-chicago-hackathon"
ds_client = datastore.Client(gcp_project_id)

response = requests.get("https://data.cityofchicago.org/resource/c4ep-ee5m.json")

crime_data = json.loads(response.text)
for crime in crime_data:
    ds_crime = datastore.Entity(key=ds_client.key('crime', crime['case_number']))
    for key, val in crime.iteritems():
        if type(val) is dict:
            ds_crime[key] = datastore.Entity(key=ds_client.key(key))
            for nest_key, nest_val in val.iteritems():
                ds_crime[key][nest_key] = nest_val
        else:
            ds_crime.update({key: val})
    
    ds_client.put(ds_crime)