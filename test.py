import requests

NOTION_TOKEN = ""
DB_ID = ""

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def update_page(page_id: str, property_name: str, new_content: str):
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

page_id = "b32a6601-fb2a-494f-9607-d157180912b3" 
property_name = "Montag"
new_content = "T12"

response = update_page(page_id, property_name, new_content)
print(response.status_code)
