import requests
import os
import pprint

NOTION_KEY = "get from key file"


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
pprint.pprint(response.json())


if response.status_code == 200:
    extract_id = response.json().get("id")
    print("Upload successfuly started, upload id: " + extract_id)
else:
    print("Upload failed:", response.status_code, response.text)
    extract_id = None


    
file_url = "https://m.media-amazon.com/images/I/71sB0CtpCcL._AC_SY240_.jpg"
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

        url = f"https://api.notion.com/v1/file_uploads/{extract_id}/send"
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
