# Convert the times into the corresponding Notion Databse row IDs
def parseTime(time):
    time_mapping = {
        "07:45-08:30": "",
        "08:30-09:15": "",
        "09:35-10:20": "",
        "10:20-11:05": "",
        "11:25-12:10": "",
        "12:15-13:00": "",
        "13:05-13:50": "",
        "13:55-14:40": "",
        "14:45-15:30": "",
        "15:35-16:20": "",
        "16:25-17:10": "",
    }
    
    return time_mapping.get(time)

# Convert the weekdays into the corresponding Notion Databse property name
def parseDate(date):
    date_mapping = {
        "Monday": "Montag",
        "Tuesday": "Dienstag",
        "Wednesday": "Mittwoch",
        "Thursday": "Donnerstag",
        "Friday": "Freitag",
    }
    
    return date_mapping.get(date)