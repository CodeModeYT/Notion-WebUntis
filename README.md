<p align="left">
    <img src="imgs/Notion_app_logo.png" height="40px" style="margin-right: 20px"/>
    <img src="imgs/WebUntis-Logo.png" width="auto" height="40px"/>
</p>

# Notion-WebUntis
Easily integrate your WebUntis timetable into your Notion Baords!

## Setup:

1. Clone / Download this repository and navigate to the directory
2. Install the dependencies using pip: `pip install -r requirements.txt`
3. Create a new [Notion integration](https://www.notion.so/my-integrations)
4. Copy the API token into the `config.json` file
5. Duplicate the [Notion template](https://outstanding-airmail-bed.notion.site/Notion-WebUntis-3429155c2d0f4fb4a2432db400eef4e9) into your own Notion board
6. Copy the [Database ID](https://developers.notion.com/reference/retrieve-a-database) (of the database in *your* Notion board) into the `config.json` file
7. Adjust `subjects.json` to match your classes with the names they have been given on WebUntis
8. Adjust `timeFormat.py` to match the class times at your school

*If you modify the structure of the database template, ensure that corresponding changes are made in `timeFormat.py`!*

## Usage:
After completing the steps listed in [Setup](#setup), simply run `main.py` and wait for the program to complete.

*If you want the program to automatically update the timetable at regular intervals, you will need to check with your school's IT department first to avoid any rate limits or even slowing down WebUntis for the entire school. Please note that I am not responsible for any damage caused by (parts of) this project.*

## Error handling:
If the Notion API returns status codes other than `200` (like most common: `400`), it is most likely caused by  the configuration in `timeFormat.py` being wrong.
Double check that the Day- and Time mapping is matching with the databse in your Notion board; especially concerning row IDs and property names. 


