import json
import webuntis
from webuntis.errors import *
from datetime import datetime, timedelta
from modules.timeFormat import parseTime, parseDate
from modules.notion import updatePage

# Calculate the date range for the current week (Monday to Friday)
today = datetime.now()
monday = today - timedelta(days=today.weekday())
friday = monday + timedelta(days=4)

# Load configuration
with open('config/config.json') as config_file:
    try:
        config = json.load(config_file)
        print("Config loaded successfully")
    except json.JSONDecodeError as e:
        print("Error loading config.json:", e)
        exit(1)
        
# Load the (whitelisted) subjects
with open('config/subjects.json') as subjects_file:
    try:
        subjects = json.load(subjects_file)
        print("Subjects loaded successfully")
    except json.JSONDecodeError as e:
        print("Error loading subjects.json:", e)
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
    print("Login successful.")
    
    # Fetch the class object
    try:
        klasse = s.klassen().filter(name=config['untis']['class_name'])[0]
        print(f"Class '{config['untis']['class_name']}' found.")
    except IndexError:
        print(f"Error: Class '{config['untis']['class_name']}' not found.")
        exit(1)

    # Fetch the timetable for the current week
    try:
        timetable = s.timetable(klasse=klasse, start=monday, end=friday)
        print("Timetable fetched successfully.")
    except Exception as e:
        print(f"Error fetching timetable: {e}")
        exit(1)

    # Loop through all the periods
    for period in timetable:
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
            print(f"PC: {period.code}")
            page_id = parseTime(f"{start_time}-{end_time}")
            property_name = parseDate(weekday)
            new_content = f"{subject}{teacher}{room}"
            annotations = {
                "italic": True,
                "strikethrough": True
            }
            # Send the data to the Notion API
            response = updatePage(page_id, property_name, new_content, annotations)
            print(response.status_code)
            continue  

        # Format periods that are irregular
        if period.code == "irregular":
            print(f"PC: {period.code}")
            page_id = parseTime(f"{start_time}-{end_time}")
            property_name = parseDate(weekday)
            new_content = f"{subject}{teacher}{room}"
            annotations = {
                "bold": True
            }
            # Send the data to the Notion API
            response = updatePage(page_id, property_name, new_content, annotations)
            print(response.status_code)
            continue 
        
        # Find the correct cell in the database to enter the data into
        page_id = parseTime(f"{start_time}-{end_time}")
        property_name = parseDate(weekday)
        new_content = f"{subject}{teacher}{room}"

        # Send the data to the Notion API
        response = updatePage(page_id, property_name, new_content)
        print(response.status_code)

# After everything is done: log out of the WebUntis Session
finally:
    s.logout()
    print("Logged out successfully.")
