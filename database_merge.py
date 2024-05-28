import os
from services.backend.src.wrappers.Wildbook import Wildbook
import pandas as pd
from pathlib import Path
import sqlite3

def create_db_from_excel(excel_path, db_path, table_name='Encounter'):
    # Read the Excel file and extract the specified columns
    df = pd.read_excel(excel_path, usecols=["SightingID", "ID", "AnnotID"])

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table in the database with the specified columns
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            SightingID TEXT,
            SealID TEXT,
            WildbookID TEXT
        )
    ''')

    # Insert the data from the DataFrame into the database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

wildbook = Wildbook(url="http://localhost:84")

def list_directories(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]


def list_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def seal_annotation(image_id_list, name_list):
    # Get images size
    images_size = wildbook.get_images_size(image_id_list)

    box_list = [[0, 0] + list(image) for image in images_size]

    # Detect the seal in the image
    aid_list = wildbook.create_annotations(image_id_list, box_list, name_list)

    return aid_list


def find_matching_name(excel_path, search_path, path_column="photo", name_column="ID"):
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

def merge_annotation_ids(excel_path, names_list, annotation_ids, output_path):
    df = pd.read_excel(excel_path, sheet_name='Sheet1')

    # Update the Annotation IDs based on the names list
    for name, annot_id in zip(names_list, annotation_ids):
        mask = (df['ID'] == name) & (df['AnnotID'].isna() | (df['AnnotID'] == ''))
        if mask.any():
            first_index = mask.idxmax()  # Get the index of the first True in the mask
            df.at[first_index, 'AnnotID'] = annot_id

    # Save the updated dataframe back to an Excel file
    df.to_excel(output_path, index=False)

# Define the path to the Excel file
excel_path = "./legacy_database/merged_file.xlsx"

def upload_files(root_dir):
    names = []
    images_id = []

    subdirs = list_directories(root_dir)
    for subdir in subdirs:
        subdir_path = os.path.join(root_dir, subdir)
        files = list_files(subdir_path)
        for file in files:
            if file.lower().endswith(
                (".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG")
            ):
                stem = Path(file).stem

                names.append(find_matching_name(excel_path, subdir + "\\" + stem))
                images_id.append(wildbook.upload_image(subdir_path + "/" + file))
    # Fix names
    names = [name if name else "Unknown" for name in names]

    annot_ids = seal_annotation(images_id, names)
    return annot_ids, names

def get_annot_ids():
    annotation_dict = {}  # Dictionary to store names and their associated IDs

    for id in range(1, 5446):
        annot_name = wildbook.get_annotation_name(f"{id}")  # Get the annotation name
        if annot_name in annotation_dict:
            annotation_dict[annot_name].append(id)  # Add ID to the existing list of IDs
        else:
            annotation_dict[annot_name] = [id]  # Create a new list with the current ID

    return annotation_dict

def add_annot_id_excel():
    names = []
    ids = []
    for id in range(1, 5446):
        annot_name = wildbook.get_annotation_name(f"{id}")
        names.append(annot_name)
        ids.append(id)

    merge_annotation_ids(excel_path, names, ids, './legacy_database/new_merged_file.xlsx')
        

#print(add_annot_id_excel())
create_db_from_excel('./legacy_database/new_merged_file.xlsx', 'output_database.db')
#annot_ids_centre, centre_names = upload_files("/Users/luukw/Documents/Rijksuniversiteit Groningen/Computing Science/Year 2/Software Engineering/Project/seal_demo/newpic")
#merge_annotation_ids(excel_path, centre_names, annot_ids_centre, './legacy_database/updated_merged_file.xlsx')
#annot_ids_field, field_names = upload_files("/Users/luukw/Documents/Rijksuniversiteit Groningen/Computing Science/Year 2/Software Engineering/Project/IDfield/seal_demo/newpic")
#merge_annotation_ids(excel_path, field_names, annot_ids_field, './legacy_database/updated_merged_file.xlsx')