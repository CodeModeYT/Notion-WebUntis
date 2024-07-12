import requests
import json
from .notion import get_checkbox_status, update_checkbox_status

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

def toggleSettingDisplay():
    # If the setting to only display periods that are happening is switched to on
    if get_checkbox_status(config['notion_page']['settings_onlynoncanc_cb_id']):
        update_checkbox_status(config['notion_page']['settings_onlycanc_cb_id'], False)
        print("Only cancs updated")
    
    # If the setting to only display periods that are NOT happening is switched to on
    if get_checkbox_status(config['notion_page']['settings_onlycanc_cb_id']):
        update_checkbox_status(config['notion_page']['settings_onlynoncanc_cb_id'], False)
        print("Only non cancs updated")
    
    else:
        return
