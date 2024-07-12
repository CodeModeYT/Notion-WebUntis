# You can use this script to retrieve the Database ID of the database the timetable should be entered into
import requests
import json

with open('config\config.json') as config_file:
    try:
        config = json.load(config_file)
        print("Config loaded successfully:")
        print(config)
    except json.JSONDecodeError as e:
        print("Error loading config.json:", e)

NOTION_TOKEN = config['notion_api']['api_token']
DB_ID = config['notion_api']['database_id']

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def search_databases():
    url = "https://api.notion.com/v1/search"
    payload = {
        "filter": {
            "value": "database",
            "property": "object"
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.json()

# Get the list of databases
databases = search_databases()

print(databases)

# Print the IDs and names of all databases
if 'results' in databases:
    for db in databases['results']:
        print(f"Database ID: {db['id']}, Name: {db['title'][0]['plain_text']}")
else:
    print("No databases found or an error occurred.")
