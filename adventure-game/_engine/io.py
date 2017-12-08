import json

# reads a file at a specified path and exports its contents to json
# returns json object if successful, None otherwise
def loadJsonFromFile(file_path):
    try:
        with open (file_path, 'r') as in_file:
            rawStringContents = in_file.read()
            return json.loads(rawStringContents)
    except:
        return None

# writes a file at a specified path filled with supplied json
# returns true if successful, false otherwise
def saveJsonToFile(file_path, json_object):
    try:
        with open (file_path, 'w') as out_file:
            # when using json."dump to string", indent=4 specifies tab spacing
            # this will result in a nicely formatted human readible file
            rawStringContents = json.dumps(json_object, indent=4)
            out_file.write(rawStringContents)
        result = True
    except:
        result = False
    return result
