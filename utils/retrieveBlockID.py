# You can use this script to retrieve the BlockID of the Block where the 'Last Updated' time should be displayed
import requests

NOTION_API_KEY = ''
PAGE_ID = ''

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def fetch_page_content(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch page content.")
        print(response.json())
        return None

def extract_block_ids(page_content):
    block_ids = []
    
    if 'results' in page_content:
        for block in page_content['results']:
            block_id = block['id']
            block_type = block['type']
            text = ""
            if block_type == 'paragraph' and 'paragraph' in block and 'rich_text' in block['paragraph']:
                if len(block['paragraph']['rich_text']) > 0:
                    text = block['paragraph']['rich_text'][0]['text']['content']
            block_ids.append({'id': block_id, 'type': block_type, 'text': text})
    
    return block_ids

def main():
    page_content = fetch_page_content(PAGE_ID)
    
    if page_content:
        block_ids = extract_block_ids(page_content)
        
        print("Block IDs and their content:")
        for block in block_ids:
            print(f"ID: {block['id']}, Type: {block['type']}, Text: {block['text']}")

if __name__ == "__main__":
    main()
