from modules.timeFormat import parseTime, parseDate
from modules.notion import updatePage

page_id = parseTime("07:45-08:30")
property_name = "Dienstag"
new_content = "Deutsch"

response = updatePage(page_id, property_name, new_content)
print(response.status_code)