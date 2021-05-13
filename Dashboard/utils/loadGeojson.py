import json

def LoadGeojson(file_name):
    # Lecture du fichier GeoJSON
    file = open(file_name)
    gj = json.load(file)
    return(gj)