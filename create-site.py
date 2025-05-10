#Modules
import json
import os
from notion_client import Client # type: ignore
import requests # type: ignore
import pprint # type: ignore

#Defining basic functions
def n_log(data):
    formatted_data = pprint.pprint(data)
    print(formatted_data)

#The next two vars are used to get the data from the request body. comment them out if test on local
try:
    jsonBody = os.getenv("BODY") or open("test-data.json").read()
except FileNotFoundError:
    raise Exception("No BODY env var and test-data.json not found.")
body = json.loads(jsonBody)
#Notion API Auth
#Comment this out if you are testing locally
#notion = Client(os.getenv("AUTH_TOKEN"))
notion = Client(auth="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") 
#Get the API token from api-token.txt file if testing locally
#JSON Processer
def get_data_from_body(data, *keys):
    for key in keys:
        data = data.get(key)
        n_log(data)
        if data is None:
            return None
    return data
#Defining the variables
site_title = get_data_from_body(body,"body","library_name")
contact_url="mailto:"+get_data_from_body(body,"body","contact_us")



#Creating the page
new_site = notion.pages.create(
    parent={"database_id":"1eea8862883480d190ecf7ce81c0a448" },
    properties={
        "Name":{
            "title": [
                {
                    "text": {
                        "content": f"Welcome to the {site_title}"
                    }
                }
            ]
        }
    }
    
)
#Appending Content to the main page
#Creating th contact us db
contact_us_db = notion.databases.create(
    parent={"page_id": new_site["id"]},
    title=[
        {
            "text": {
                "content": "Contact Us"
            }
        }
    ],
    properties={
        "Name": {
            "title": {}
        },
        "super:Link":{
            type: "url"
        }
    }
)
#Appending the first paragraph INCOMPLETE
first_paragraph = notion.blocks.children.append(
    block_id=new_site["id"],
    children=[]
)
#Adding toggles INCOMPLETE
first_toggles = notion.blocks.children.append(
    block_id=new_site["id"],
    children=[]
)

#Adding the contact us toggle
contact_toggle = notion.blocks.children.append(
    block_id=new_site["id"],
    children=[
        {
            "type": "toggle",
            "toggle": {
                "text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Contact Us"
                        }
                    }
                ]
            }
        }
    ]
)
toggle_id = contact_toggle["results"][0]["id"]
notion.blocks.children.append(
    block_id=toggle_id,
     children=[
        {
            "object": "block",
            "type": "linked_database",
            "linked_database": {
                "database_id": contact_us_db["id"],
            }
        }
    ]
)

#Adding event page
upcomming_events = notion.pages.create(
    parent={"page_id": new_site["id"]},
    properties={
            "title": [
                {
                    "text": {
                        "content": "Upcoming Events"
                    }
                }
            ]
        
    }
)
#adding contact bottons
notion.pages.create(
    parent={"database_id": contact_us_db["id"]},
    properties={
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "Contact Us"
                    }
                }
            ]
        },
        "super:Link": {
            "url": contact_url
        }
    }
)


