import os
import re
import json

def remove_html_tags(text):
    # Pattern to find HTML tags
    pattern = re.compile(r'<[^>]+>')
    # Replace HTML tags with an empty string
    return pattern.sub('', text)

dir_path = '/home/joyv/scriptie/spade_source_copy'
output_dir_path = '/home/joyv/scriptie/spade_output'  # replace with the path to the text file where you want to save the output

# Iterate over all files in the directory
for filename in os.listdir(dir_path):
    # Check if the file is a JSON file
    if filename.endswith('.json'):
        # Full path to the JSON file
        file_path = os.path.join(dir_path, filename)
        # Full path to the output TXT file
        output_file_path = os.path.join(output_dir_path, f'{os.path.splitext(filename)[0]}.txt')

        with open(file_path, 'r') as file:
            data = json.load(file)
            text = data.get('split_pages_strings', [])

        # Save the output to a text file
        with open(output_file_path, 'w') as output_file:
            

            for i in text:
                i = remove_html_tags(i)

                print(i)
                output_file.write(i)