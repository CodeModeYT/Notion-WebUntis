import requests

NOTION_TOKEN = ""
DB_ID = ""

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
