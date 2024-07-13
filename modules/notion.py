import requests
import json

# Open the config file
with open('config\config.json') as config_file:
    try:
        config = json.load(config_file)
        print("Config loaded successfully:")
        print(config)
    except json.JSONDecodeError as e:
        print("Error loading config.json:", e)

# Read the content file and declare the config variables
NOTION_TOKEN = config['notion_api']['api_token']
DB_ID = config['notion_api']['database_id']

# Build the Notion API request
headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def updatePage(page_id: str, property_name: str, new_content: str, annotations: dict = None):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    text_object = {
        "type": "text",
        "text": {
            "content": new_content,
        }
    }

    if annotations:
        text_object["annotations"] = annotations

    payload = {
        "properties": {
            property_name: {
                "rich_text": [
                    text_object
                ]
            }
        }
    }

    res = requests.patch(url, json=payload, headers=headers)
    return res

def clearPage(page_id: str, property_name: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    text_object = {
        "type": "text",
        "text": {
            "content": "",
        }
    }
    payload = {
        "properties": {
            property_name: {
                "rich_text": [
                    text_object
                ]
            }
        }
    }
    res = requests.patch(url, json=payload, headers=headers)
    return res

def updateParagraph(id, content):
    url = f"https://api.notion.com/v1/blocks/{id}"
    
    payload = {
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": content
                    }
                }
            ]
        }
    }
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        exit
    else:
        print("Failed to update text:")
        print(response.json())
        
def get_checkbox_status(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        block = response.json()
        if block["type"] == "to_do":
            return block["to_do"]["checked"]
        else:
            raise Exception("The block is not a to_do block with a checkbox.")
    else:
        raise Exception(f"Failed to retrieve block: {response.status_code}, {response.text}")

def update_checkbox_status(block_id, checked):
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    data = {
        "to_do": {
            "checked": checked
        }
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        exit
    else:
        print(f"Failed to update checkbox status: {response.status_code}")
        print(response.json())
