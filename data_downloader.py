import requests
from tqdm import trange, tqdm
import json
import os

# Create a bucket to store our data into
data = []

# Check if dataset file already exists
dataset_name = 'rick_and_morty_dataset.json'
if not os.path.exists(dataset_name):

    # Fetch data from API and store it in 'data' list
    total_number_of_pages = 42
    for page in trange(total_number_of_pages, desc="Fetching dataset."):
        response = requests.get(f"https://rickandmortyapi.com/api/character/?page={page}")
        data.extend(response.json()["results"])

    # Save the 'data' list as JSON file
    with open(dataset_name, 'w') as f:
        json.dump(data, f)

# Check if image directory exists
images_path = 'images'
if not os.path.exists(images_path):
    os.mkdir(images_path)

# Download and save images from the 'data' list
for avatar in tqdm(data, desc="Downloading Images"):
    try:
        image_url = avatar['image']
        image_filename = image_url.split('/')[-1]
        image_content = requests.get(image_url).content

        with open(f"{images_path}/{image_filename}", 'wb') as f:
            f.write(image_content)

    except Exception as e:
        print(e)
