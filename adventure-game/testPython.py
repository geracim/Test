import json

with open ('pythonData.txt', 'r') as in_file:
    rawStringContents = in_file.read()
    jsonContents = json.loads(rawStringContents)

    state = input()

    print( jsonContents[state] )