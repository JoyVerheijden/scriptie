import img2pdf
import re
import tempfile
import logging
import os
import tools
import fitz
from pathlib import Path
import json
from transformers import BertTokenizer


# Convert pdf to layout-preserving .txt file
# Written by Spadework
def pdf_to_lptext(file_contents, mode="layout", pages=False):
    if pages:
        pages = []
        with tempfile.NamedTemporaryFile(suffix=".pdf") as file:
            logging.info(f"Created temporary file {file.name}")
            file.write(file_contents)
            file.flush()

            p = 1
            while True:
                cmd = (
                    f"python3 -m fitz gettext -mode {mode} -convert-white"
                    f" -pages {p} {file.name}"
                )
                process = os.system(cmd)
                if process != 0:
                    break
                p += 1
                fn = Path(file.name).with_suffix(".txt")
                page_text = open(
                    fn, "r"
                ).read()
                pages.append(page_text)
                os.unlink(fn)
        return pages
    else:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as file:
            logging.info(f"Created temporary file {file.name}")
            file.write(file_contents)
            file.flush()

            cmd = (
                f"python3 -m fitz gettext -mode {mode} -convert-white"
                f" -extra-spaces {file.name}"
            )
            process = os.system(cmd)
            #if process != 0:
            #    raise Exception(f"Parse failed: {process}")
            fn = Path(file.name).with_suffix(".txt")
            text = open(fn, "r").read()
            os.unlink(fn)

        print
        return text

# Create temp_bbox.txt file from layout-preserving text
def lptxt_to_bbox(lptext):

    with open("temp_bbox.txt", 'w') as bbox_file:

        # scale factor
        scale_factor = 10

        for y1, line in enumerate(lptext.splitlines(), start=1):

            # Remove HTML tags
            line = re.sub('<[^<]+?>', '', line)

            # Split the line into words
            words = line.strip().split()
            for word in words:
                # Get the starting position of the word in the line
                x1 = line.find(word)

                # Write the word, its location, and its length to the output file
                X2 = (x1 + len(word)) * scale_factor
                Y2 = (y1 + 1) * scale_factor
                X1 = x1 * scale_factor
                Y1 = y1 * scale_factor
                
                bbox_file.write(f'{word} {X1} {Y1} {X2} {Y2}\n')


# Take temp_bbox.txt file and creates 2 json files: 
# One for layout information (bboxes) and the other for text information
def bbox_to_json(json_path_layout, json_path_text):
    # Initialize the list of bounding boxes
    bboxes = []
    words_list = []

    # Read the bounding boxes from the file
    with open('temp_bbox.txt', 'r') as bbox_file:
        for line in bbox_file:
            
            # Split the line into words
            parts = line.strip().split()
            # Append the word to the words list
            words_list.append(parts[0])
            # Remove the first word and convert the coordinates to floats
            coords = list(map(float, parts[1:]))

            # Append the coordinates to the bounding boxes list
            bboxes.append(coords)

    os.remove('temp_bbox.txt')

    """
    rescale to [595, 842]
    """
    new_bboxes = []
    max_x = 0
    max_y = 0

    for bbox in bboxes:
        max_x = max(max_x, bbox[2])
        max_y = max(max_y, bbox[3])

    scale_factor_x = 595 / max_x
    scale_factor_y = 842 / max_y

    for i, bbox in enumerate(bboxes):
        new_bbox = [int(round(bbox[0] * scale_factor_x)), int(round(bbox[1] * scale_factor_y)), int(round(bbox[2] * scale_factor_x)), int(round(bbox[3] * scale_factor_y))]
        new_bboxes.append(new_bbox)
    
    bboxes = new_bboxes

    # Convert the list of words to a string
    words_string = ' '.join(words_list)

    # Write the bounding boxes to the JSON file
    with open(json_path_layout, 'w') as json_file:
        json.dump({'src': bboxes, 'tgt': bboxes} , json_file)  

    # Write the words and other data to the second JSON file
    with open(json_path_text, 'w') as json_file_2:

        original_filename = "file"

        json.dump({
            'bleu': 1,
            'filename': original_filename,
            'original_filename': original_filename,
            'page_idx': 0,
            'src': words_string,
            'tgt': words_string,
            'tgt_index': list(range(0, len(words_string.split())))
        }, json_file_2)


# Take pdf and use pdf_to_lptext(), lptxt_to_bbox() and bbox_to_json() to create json files 
def pdf_to_json(pdf_path, json_path_layout, json_path_text):
    # Convert the PDF to text and layout
    with open(pdf_path, 'rb') as file:
        file_contents = file.read()
    
    page_text = pdf_to_lptext(file_contents)

    #print(page_text)

    # Convert the text to bounding boxes
    lptxt_to_bbox(page_text)

    # Convert the bounding boxes to JSON
    bbox_to_json(json_path_layout, json_path_text)


pdf_path = '/home/joyv/scriptie/resume_english/19.pdf'
with open(pdf_path, 'rb') as file:
    file_contents = file.read()

page_text = pdf_to_lptext(file_contents)
print(page_text)


# # Take map of pdfs and convert into map with jsons
# def convert_pdfs_to_jsons():

#     pdf_dir = 'resume_english'
#     json_dir = 'temp_jsons'

#     # Delete the contents of json_dir
#     for file in os.listdir(json_dir):
#         file_path = os.path.join(json_dir, file)
#         if os.path.isfile(file_path):
#             os.remove(file_path)


#     pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

#     for i, pdf_file in enumerate(pdf_files, start=1):


#         pdf_path = os.path.join(pdf_dir, pdf_file)
#         json_path_layout = os.path.join(json_dir, f'dataset-test-s2s-layout-m{i}.json')
#         json_path_text = os.path.join(json_dir, f'dataset-test-s2s-text-m{i}.json')
#         pdf_to_json(pdf_path, json_path_layout, json_path_text)



def convert_pdfs_to_jsons(pdf_dir = 'resume_english2', json_dir = 'temp_jsons'):

    # Iterate over all files in the directory
    for filename in os.listdir(pdf_dir):
        # Check if the file is a PDF
        if filename.endswith('.pdf'):
            # Full path to the PDF file
            pdf_path = os.path.join(pdf_dir, filename)
            # Full paths to the output JSON files


            json_path_layout = os.path.join(json_dir, f'dataset-test-s2s-layout-m{os.path.splitext(filename)[0]}.json')
            json_path_text = os.path.join(json_dir, f'dataset-test-s2s-text-m{os.path.splitext(filename)[0]}.json')

            # Convert the PDF to JSON
            pdf_to_json(pdf_path, json_path_layout, json_path_text)


#convert_pdfs_to_jsons()


# # Directory containing the PDF files
# pdf_dir = '/home/joyv/scriptie/resume_english'

# # Iterate over all files in the directory
# for filename in os.listdir(pdf_dir):
#     # Check if the file is a PDF
#     if filename.endswith('.pdf'):
#         # Full path to the PDF file
#         pdf_path = os.path.join(pdf_dir, filename)
#         # Full path to the output TXT file
#         txt_path = os.path.join(pdf_dir, f'{os.path.splitext(filename)[0]}.txt')

#         # Open the PDF file in binary mode and read its contents
#         with open(pdf_path, 'rb') as pdf_file:
#             pdf_contents = pdf_file.read()

#         # Extract the text from the PDF
#         page_text = pdf_to_lptext(pdf_contents)

#         # Open the TXT file in write mode and write the text to it
#         with open(txt_path, 'w') as txt_file:
#             txt_file.write(page_text)
        