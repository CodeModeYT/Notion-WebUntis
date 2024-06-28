import requests

NOTION_TOKEN = ""
DB_ID = ""

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