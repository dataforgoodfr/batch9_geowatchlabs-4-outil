import json

def LoadGeojson(file_name):
    # Lecture du fichier GeoJSON
    file = open(file_name)
    gj = json.load(file)
   # for i in range(len(gj['features'])):
   #     name = gj['features'][i]['properties']['NAME_2']
   #     name_corrected = name.encode("latin_1").decode("utf_8")
   #     gj['features'][i]['properties']['NAME_2'] = name_corrected
    return(gj)