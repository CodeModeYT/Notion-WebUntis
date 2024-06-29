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

def updatePage(page_id: str, property_name: str, new_content: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            property_name: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": new_content,
                        }
                    }
                ]
            }
        }
    }
    res = requests.patch(url, json=payload, headers=headers)
    return res
