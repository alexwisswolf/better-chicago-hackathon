from google.cloud import datastore
import xlrd
import requests

gcp_project_id = "better-chicago-hackathon"
ds_client = datastore.Client(gcp_project_id)

response = requests.get("http://cps.edu/Performance/Documents/Datafiles/psae_schools_FINAL_2001_to_2014_Overall_With_ELL_20140819.xls")

workbook = xlrd.open_workbook(file_contents=response.content)

sheet = workbook.sheet_by_index(0)
max_row = max(0, sheet.nrows)
cols = [
    "school_name",
    "school_id",
    "unit",
    "network",
    "category",
    "category_breakdown",
    "grade",
    "year",
    "meet_exceed_read",
    "meet_exceed_math",
    "meet_exceed_science",
    "meet_exceed_composite",
    "exceed_read",
    "exceed_math",
    "exceed_science",
    "exceed_composite",
    "meet_read",
    "meet_math",
    "meet_science",
    "meet_composite",
    "below_read",
    "below_math",
    "below_science",
    "below_composite",
    "warn_read",
    "warn_math",
    "warn_science",
    "warn_composite",
    "total_tested_read",
    "total_tested_math",
    "total_tested_science",
    "total_tested_composite"
]

for row in range(2,max_row):
    row_dict = {}
    for header, col in zip(cols, sheet.row(row)):
        if header in ['year', 'school_id', 'unit', 'total_tested_read', 'total_tested_math', 'total_tested_science', 'total_tested_composite']:
            row_dict[header] = int(col.value)
        else:
            row_dict[header] = col.value
    
    with ds_client.transaction():
        ds_psae = datastore.Entity(ds_client.key('psae', str(row_dict['school_id']) + str(row_dict['year'])))
        ds_psae.update(row_dict)
        ds_client.put(ds_psae)