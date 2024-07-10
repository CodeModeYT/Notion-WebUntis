# You can use this script to retrieve the Page ID of the certain Notion page where you want the timetable to be located
import requests
import json

with open('config\config.json') as config_file:
    try:
        config = json.load(config_file)
        print("Config loaded successfully:")
        print(config)
    except json.JSONDecodeError as e:
        print("Error loading config.json:", e)

NOTION_TOKEN = config['notion']['api_token']
DB_ID = config['notion']['database_id']

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def query_database(database_id: str):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.post(url, headers=headers)
    return res.json()

# Get the list of pages in the database
pages = query_database(DB_ID)
print(pages)

if 'results' in pages:
    for page in pages['results']:
        print(page['id'])
else:
    print("No results found or an error occurred.")
