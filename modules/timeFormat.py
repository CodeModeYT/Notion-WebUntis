# Convert the times into the corresponding Notion Databse row IDs
def parseTime(time):
    time_mapping = {
        "07:45-08:30": "3a051125-1484-41a0-8367-cc1673ed0ba4",
        "08:30-09:15": "b32a6601-fb2a-494f-9607-d157180912b3",
        "09:35-10:20": "8616cc57-d402-425f-add7-2e5f1b375aaf",
        "10:20-11:05": "1850ab52-0ad9-4eb2-8bbc-2a47d2a5314b",
        "11:25-12:10": "c5956407-e47d-49fa-9ca4-430f45e6ec1d",
        "12:15-13:00": "6cc52eb3-7da3-41e9-bbf8-430b2b68f199",
        "13:05-13:50": "4a1c67ac-c48a-44f2-a38d-77179a634c9c",
        "13:55-14:40": "ad53be70-753d-48e1-82bd-1282128bedb2",
        "14:45-15:30": "5893f071-ad58-4e32-8651-a99e7be9452a",
        "15:35-16:20": "939de459-5f3a-441b-b59f-ff7e9ea716d7",
        "16:25-17:10": "4c6227e1-bd4c-4ceb-8d6e-1960e0366405",
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