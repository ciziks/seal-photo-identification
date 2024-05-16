from typing import List, Tuple
from antidote import inject
import requests
import os
from services.backend.src.wrappers.Wildbook import Wildbook
import pandas as pd
from pathlib import Path

wildbook = Wildbook()

def list_directories(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def list_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def seal_annotation(image_id_list, name_list):
    # Get images size
    images_size = wildbook.get_images_size(image_id_list)

    box_list = [[0,0] + image for image in images_size]

    # Detect the seal in the image
    aid_list = wildbook.create_annotations(image_id_list, box_list, name_list)

    return aid_list
    
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
excel_path = ...

def upload_files(root_dir):
    names = []
    images_id = []

    subdirs = list_directories(root_dir)
    for subdir in subdirs:
        subdir_path = os.path.join(root_dir, subdir)
        files = list_files(subdir_path)
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')):
                stem = Path(file).stem

                names.append(find_matching_name(excel_path, subdir + '\\' + stem))
                images_id.append(wildbook.upload_image(subdir_path + '/' + file))

    annot_ids = seal_annotation(images_id, names)
    return annot_ids
            

annot_ids = upload_files("/Users/luukw/Documents/Rijksuniversiteit Groningen/Computing Science/Year 2/Software Engineering/Project/seal_demo/newpic")
