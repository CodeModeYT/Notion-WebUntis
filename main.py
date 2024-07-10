import json
import webuntis
from webuntis.errors import *
from datetime import datetime, timedelta
from modules.timeFormat import parseTime, parseDate
from modules.notion import updatePage, updateParagraph
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init()

# Calculate the date range for the current week (Monday to Friday)
today = datetime.now()
monday = today - timedelta(days=today.weekday())
friday = monday + timedelta(days=4)

# Load configuration
with open('config/config.json') as config_file:
    try:
        config = json.load(config_file)
        tqdm.write("Config loaded successfully")
    except json.JSONDecodeError as e:
        tqdm.write(f"Error loading config.json: {e}")
        exit(1)
        
# Load the (whitelisted) subjects
with open('config/subjects.json') as subjects_file:
    try:
        subjects = json.load(subjects_file)
        tqdm.write("Subjects loaded successfully")
    except json.JSONDecodeError as e:
        tqdm.write(f"Error loading subjects.json: {e}")
        exit(1)

# Create a session and login
s = webuntis.Session(
    server=config['untis']['server'],
    username=config['untis']['username'],
    password=config['untis']['password'],
    school=config['untis']['school'],
    useragent='Notion-WebUntis'
)

try:
    # Log into the WebUntis Session
    s.login()
    tqdm.write("Login successful.")
    
    # Fetch the class object
    try:
        klasse = s.klassen().filter(name=config['untis']['class_name'])[0]
        tqdm.write(f"Class '{config['untis']['class_name']}' found.")
    except IndexError:
        tqdm.write(f"Error: Class '{config['untis']['class_name']}' not found.")
        exit(1)

    # Fetch the timetable for the current week
    try:
        timetable = s.timetable(klasse=klasse, start=monday, end=friday)
        tqdm.write("Timetable fetched successfully.")
    except Exception as e:
        tqdm.write(f"Error fetching timetable: {e}")
        exit(1)

    # Loop through all the periods and displaying a progress bar
    for period in tqdm(timetable, desc=f"{Fore.BLUE}Updating periods{Style.RESET_ALL}", unit="period", bar_format="{l_bar}{bar}{r_bar}"):

        # Skip subjects that are not whitelisted
        whitelist_subjects = subjects['subjects']
        if any(subj.name not in whitelist_subjects for subj in period.subjects):
            continue
        
        # Format the time given by WebUntis
        weekday = period.start.strftime('%A')
        start_time = period.start.strftime('%H:%M')
        end_time = period.end.strftime('%H:%M')
        
        # Format the API responses for use in the database
        # (Commas are added here so it doesn't look weird if one aspect is missing)
        subject = period.subjects[0].name + ', ' if period.subjects and period.teachers else (period.subjects[0].name if period.subjects and not period.teachers else '')
        teacher = period.teachers[0].name if period.teachers else ''
        room = ''
        try:
            if period.rooms:
                # (Comma is added here so it doesn't look weird if one aspect is missing)
                room = ', '+period.rooms[0].name
        except IndexError:
            room = ''
        
        # Format subjects that are cancelled
        if period.code == "cancelled":
            tqdm.write(f"PC: {period.code}")
            page_id = parseTime(f"{start_time}-{end_time}")
            property_name = parseDate(weekday)
            new_content = f"{subject}{teacher}{room}"
            annotations = {
                "italic": True,
                "strikethrough": True
            }
            # Send the data to the Notion API
            response = updatePage(page_id, property_name, new_content, annotations)
            tqdm.write(str(response.status_code))
            continue  

        # Format periods that are irregular
        if period.code == "irregular":
            tqdm.write(f"PC: {period.code}")
            page_id = parseTime(f"{start_time}-{end_time}")
            property_name = parseDate(weekday)
            new_content = f"{subject}{teacher}{room}"
            annotations = {
                "bold": True
            }
            # Send the data to the Notion API
            response = updatePage(page_id, property_name, new_content, annotations)
            tqdm.write(str(response.status_code))
            continue 
        
        # Find the correct cell in the database to enter the data into
        page_id = parseTime(f"{start_time}-{end_time}")
        property_name = parseDate(weekday)
        new_content = f"{subject}{teacher}{room}"

        # Send the data to the Notion API
        response = updatePage(page_id, property_name, new_content)
        tqdm.write(str(response.status_code))

# After everything is done: log out of the WebUntis Session
finally:
    s.logout()
    updateParagraph(config['notion']['la_block_id'], f"Zuletzt aktualisiert: {datetime.now().strftime("%d %b %Y %H:%M")}")
    tqdm.write(f"{Fore.GREEN}Timetable updated successfully.{Style.RESET_ALL}")
    tqdm.write(f"{Fore.GREEN}Last updated:{Style.RESET_ALL} {datetime.now()}")
