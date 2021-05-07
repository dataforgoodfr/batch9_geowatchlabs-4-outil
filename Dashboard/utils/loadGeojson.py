import geojson

def LoadGeojson(file_name):
    # Lecture du fichier GeoJSON
    file = open(file_name)
    gj = geojson.load(file)
    return(gj)