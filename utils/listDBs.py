import requests

NOTION_TOKEN = ""

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
