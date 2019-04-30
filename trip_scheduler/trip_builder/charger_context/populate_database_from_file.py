from charger_context import ChargerContext
import json, requests
"""
This file is used to populate the database from a .json file containing the charger objects. 
It will load the chargers from json, then create a postgres DB if it does not exists (a postgres db and users
must be installed previously). It will then insert the objects. 
"""


filepath = ''

def Populate():
    context = ChargerContext()
    objects = context.GetChargersFromFile(filepath)
    context.createDatabase()
    context.InsertChargers(objects)


def DownloadData(saveFilePath):
    """
    This method can be used to download charger data and save it to a JSON file. 
    """
    requestString = 'https://api.openchargemap.io/v3/poi/?output=json&countrycode=US'
    response = requests.get(requestString)
    content = response.content 
    jsonData = content.decode('utf8').replace("'", '"')
    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(jsonData)

    with open(saveFilePath, 'w') as f:
            f.write(json.dumps(data, default=ToJson, indent=4, sort_keys=False))


def ToJson(instance):
    return {k:v for k , v in vars(instance).items() if not str(k).startswith('_')}

if __name__ == "__main__":
    Populate()