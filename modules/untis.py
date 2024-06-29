import json
import webuntis
from webuntis.objects import PeriodObject
from webuntis.errors import *

with open('config\config.json') as config_file:
    try:
        config = json.load(config_file)
        print("Config loaded successfully:")
        print(config)
    except json.JSONDecodeError as e:
        print("Error loading config.json:", e)

s = webuntis.Session(
    server=config['untis']['server'],
    username=config['untis']['username'],
    password=config['untis']['password'],
    school=config['untis']['school'],
    useragent='Notion-WebUntis'
)
s.login()

klasse = s.klassen().filter(name=config['untis']['class_name'])[0]