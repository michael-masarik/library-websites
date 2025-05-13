import os
from notion_client import Client 
import requests 
import pprint 
import re

#Variables
NOTION_KEY =  os.getenv("AUTH_TOKEN")
FILE_PATH = os.getenv("FILE_URL")
notion = Client(auth=NOTION_KEY)
page_id = os.getenv("PAGE_ID")

def format_notion_id(raw_id):
    # Remove quotes if accidentally included
    raw_id = raw_id.strip().replace('"', '')

    # Add dashes if needed
    if "-" not in raw_id and len(raw_id) == 32:
        return f"{raw_id[0:8]}-{raw_id[8:12]}-{raw_id[12:16]}-{raw_id[16:20]}-{raw_id[20:]}"
    return raw_id
    

page_id = format_notion_id(page_id)
print("Formatted page_id:", page_id)

#Starting the upload for the pdf
n_upload_url = "https://api.notion.com/v1/file_uploads"

payload = {
        "filename": "events.pdf",  
        "content_type": "application/pdf"
    }    
headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {NOTION_KEY}",
        "Notion-Version": "2022-06-28"
    }

response = requests.post(n_upload_url, json=payload, headers=headers)

if response.status_code == 200:
    file_id = response.json().get("id")
    print("Upload successfuly started! Upload id: " + file_id)
else:
    print("Upload failed:", response.status_code, response.text)
    file_id = None


#Finishing the upload for the PDF    
file_url = FILE_PATH
response = requests.get(file_url, stream=True)

if response.status_code == 200:
    temp_file_path = "temp_image.pdf"
    with open(temp_file_path, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    with open(temp_file_path, "rb") as f:
        files = {
            "file": ("file.pdf", f, "application/pdf"),
        }

        url = f"https://api.notion.com/v1/file_uploads/{file_id}/send"
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


# 1. Get blocks
response = notion.blocks.children.list(block_id=page_id)
blocks = response["results"]

# 2. Extract block IDs
block_ids = [block["id"] for block in blocks]

# 3. Delete each block
for block_id in block_ids:
    notion.blocks.delete(block_id=block_id)
    print(f"Deleted block {block_id}")

# Creating PDF embed
notion.blocks.children.append(
    block_id=page_id,
    children=[
        {
            "type": "pdf",
            "pdf": {
                "type": "file_upload",
                "file_upload": {
                    "id": file_id
                }
            }
        }
    ]
)