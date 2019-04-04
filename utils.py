import json
def readJsonFile(fileName):
    json_data = open(fileName).read()
    data = json.loads(json_data)
    return data
def writeJsonFile(fileName,data):
    with open(fileName,'w+') as file:
        json.dump(data,file,indent=4)