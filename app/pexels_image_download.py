import os
import requests

PEXELS_API_KEY = 'your_api_key_here'
SEARCH_QUERY = 'your_search_here'
PER_PAGE = 80
TOTAL_IMAGES = 500
SAVE_FOLDER = 'whre_to_save'

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def download_images():
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    
    page = 1
    downloaded = 0
    
    while downloaded < TOTAL_IMAGES:
        url = f'https://api.pexels.com/v1/search?query={SEARCH_QUERY}&per_page={PER_PAGE}&page={page}'
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json()}")
            break
        
        photos = response.json().get('photos', [])
        if not photos:
            print("No more photos available.")
            break
        
        for photo in photos:
            if downloaded >= TOTAL_IMAGES:
                break
            
            image_url = photo['src']['original']
            image_id = photo['id']
            file_extension = image_url.split('.')[-1]
            file_name = f"{SAVE_FOLDER}/whatever{image_id}.{file_extension}"
            
            img_data = requests.get(image_url).content
            with open(file_name, 'wb') as handler:
                handler.write(img_data)
            
            downloaded += 1
            print(f"Downloaded {downloaded}/{TOTAL_IMAGES}: {file_name}")
        
        page += 1

download_images()
