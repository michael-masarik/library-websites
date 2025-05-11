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
NOTION_KEY =  "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" #os.getenv("AUTH_TOKEN")
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
cover_image_url = get_data_from_body(body, "body", "cover_image")
icon_image_url = get_data_from_body(body, "body", "icon_image")

#Starting the upload for the cover image
n_upload_url = "https://api.notion.com/v1/file_uploads"

payload = {
        "filename": "image.jpg",  # The extension can be either .jpeg or .jpg
        "content_type": "image/jpeg"
    }    
headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer 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",
        "Notion-Version": "2022-06-28"
    }

response = requests.post(n_upload_url, json=payload, headers=headers)

if response.status_code == 200:
    cover_image_id = response.json().get("id")
    n_log("Upload successfuly started, upload id: " + cover_image_id)
else:
    print("Upload failed:", response.status_code, response.text)
    cover_image_id = None


#Finishing the upload for the cover image    
file_url = cover_image_url
response = requests.get(file_url, stream=True)

if response.status_code == 200:
    temp_file_path = "temp_image.jpg"
    with open(temp_file_path, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    with open(temp_file_path, "rb") as f:
        files = {
            "file": ("image.jpg", f, "image/jpeg"),
        }

        url = f"https://api.notion.com/v1/file_uploads/{cover_image_id}/send"
        headers = {
            "Authorization": f"Bearer {NOTION_KEY}",
            "Notion-Version": "2022-06-28"
        }

        response = requests.post(url, headers=headers, files=files)
        pprint.pprint(response.json)

    # Delete the temporary file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
else:
    print("Failed to download the file:", response.status_code)
#Starting the upload for the icon image
n_upload_url = "https://api.notion.com/v1/file_uploads"

payload = {
        "filename": "image.jpg",  # The extension can be either .jpeg or .jpg
        "content_type": "image/jpeg"
    }    
headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer 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",
        "Notion-Version": "2022-06-28"
    }

response = requests.post(n_upload_url, json=payload, headers=headers)

if response.status_code == 200:
    icon_image_id = response.json().get("id")
    n_log("Upload successfuly started, upload id: " + icon_image_id)
else:
    print("Upload failed:", response.status_code, response.text)
    cover_image_id = None


#Finishing the upload for the cover image    
file_url = icon_image_url
response = requests.get(file_url, stream=True)

if response.status_code == 200:
    temp_file_path = "temp_image.jpg"
    with open(temp_file_path, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    with open(temp_file_path, "rb") as f:
        files = {
            "file": ("image.jpg", f, "image/jpeg"),
        }

        url = f"https://api.notion.com/v1/file_uploads/{icon_image_id}/send"
        headers = {
            "Authorization": f"Bearer {NOTION_KEY}",
            "Notion-Version": "2022-06-28"
        }

        response = requests.post(url, headers=headers, files=files)
        pprint.pprint(response.json)

    # Delete the temporary file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
else:
    print("Failed to download the file:", response.status_code)
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
#Adding the cover image to the page
notion.pages.update(
    page_id=new_site["id"],
    cover={
        "type": "file_upload",
        "file_upload": {
            "id": cover_image_id
        }
    },
    icon={
        
            "type": "file_upload",
            "file_upload": {
            "id": icon_image_id
            }
        }
    
)

#Appending first Paragraph to the main page
content = notion.blocks.children.append(
    block_id=new_site["id"],
    children=[
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

