from google.cloud import datastore
import sys
import csv
from google.cloud import datastore
from flask import Response
import xml.etree.ElementTree as ET
import json
from xml.dom import minidom



def load_ds():
    try:
        file_name = sys.argv[2]
    except IndexError:
        print "Using default filename."
        file_name = "cps_boundaries.csv"

    gcp_project_id = "better-chicago-hackathon"
    ds_client = datastore.Client(gcp_project_id)

    fusion_table_id = "1NXIcj0Eo65MNv-wczBoEMcovlsIJ1p66CfeP8JFV"

    headers = ['school_id', 'school_name', 'school_address', 'boundary_grades', 'geometry']
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            row_dict = {}
            for i in range(len(headers)):
                row_dict[headers[i]] = unicode(row[i])
            
            ds_boundary = datastore.Entity(ds_client.key('cps_boundary', str(row_dict['school_id'])), exclude_from_indexes=['geometry'])
            ds_boundary.update(row_dict)
            ds_client.put(ds_boundary)

def create_file():
    
    gcp_project_id = "better-chicago-hackathon"
    ds_client = datastore.Client(gcp_project_id)

    query = ds_client.query(kind="cps_boundary")
    results = list(query.fetch())
    root = ET.Element('kml')

    document = ET.SubElement(root, "Document")
    name = ET.SubElement(document, "name")
    name.text = "cps_boundaries.kml"
    for result in results:
        placemark = ET.SubElement(document, "Placemark")
        school_name = ET.SubElement(placemark, "name")
        school_name.text = result['school_name'].replace(" ", "_")
        geo_element = ET.fromstring(result['geometry'])
        placemark.insert(1, geo_element)
        #root.insert(0, ET.fromstring(result['geometry']))
    pretty_xml = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    #ET.ElementTree(root).write("cps_boundaries.kml")
    f = open("../assets/cps_boundaries.kml", "w")
    f.write(pretty_xml)
    f.close()

if __name__ == "__main__":
    try:
        mode = sys.argv[1]
    except IndexError:
        print "Please specify mode."
        exit(1)
    if mode == "load_ds":
        load_ds()
    elif mode == "create_file":
        create_file()
    else:
        print "Bad mode."
        exit(1)