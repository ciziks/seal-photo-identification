from typing import List, Tuple
from antidote import inject
import requests
import os
from Wildbook import Wildbook
import pandas as pd
from pathlib import Path

wildbook = Wildbook()

def list_directories(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def list_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def upload_seal(image_path: str, name: str):
    # Upload image
    image_id = wildbook.upload_image(image_path)

    image_uuid = wildbook.get_images_uuids([int(image_id)])

    image_size = wildbook.get_images_size([int(image_id)])

    # Detect the seal in the image
    aid_list = wildbook.create_annotation(image_uuid, image_size)

    #Set the name of the seal
    wildbook.rename_annotations(aid_list, [name])
    
def find_matching_name(excel_path, search_path, path_column='photo', name_column='ID'):
    # Load the Excel file
    df = pd.read_excel(excel_path)
    
    # Search for the given path in the specified column
    matching_row = df[df[path_column] == search_path]
    
    # Check if there is a matching row
    if not matching_row.empty:
        # Return the matching name
        return matching_row[name_column].values[0]
    else:
        return None

# Define the path to the Excel file
excel_path = '/Users/luukw/Documents/Rijksuniversiteit Groningen/Computing Science/Year 2/Software Engineering/Project/merged_file.xlsx'

def upload_files(root_dir):
    subdirs = list_directories(root_dir)
    for subdir in subdirs:
        subdir_path = os.path.join(root_dir, subdir)
        files = list_files(subdir_path)
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')):
                stem = Path(file).stem
                name = find_matching_name(excel_path, subdir + '\\' + stem)
                upload_seal(subdir_path + '/' + file, name)

upload_files("/Users/luukw/Documents/Rijksuniversiteit Groningen/Computing Science/Year 2/Software Engineering/Project/seal_demo/newpic")
upload_files("/Users/luukw/Documents/Rijksuniversiteit Groningen/Computing Science/Year 2/Software Engineering/Project/IDfield/seal_demo/newpic")