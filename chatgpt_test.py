import os
import openai
openai.api_key = "key"

import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt

import time
start_time = time.time()





@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None,
                            model="gpt-3.5-turbo-0613", temperature=0):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages, "temperature": temperature}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    


gpt_model = "gpt-4-0613"
### EXTRACT SKILLS FROM VACANCY ###

import os

dir_path = '/home/joyv/scriptie/dataset/lp_text/'
output_dir = '/home/joyv/scriptie/dataset/chatgpt_output_temp/'


# Iterate over all files in the directory
for filename in os.listdir(dir_path):
    # Check if the file is a text file
    if filename.endswith('.txt'):
        # Full path to the text file
        file_path = os.path.join(dir_path, filename)

        # Read the content of the file into text_file
        with open(file_path, 'r') as file:
            text_file = file.read()

        # Prepare messages for chat model
        messages = [
            {
                "role": "system",
                
                "content": 
                """My job is to read a text file and return the text in the file in the correct reading order.

                The input text is formatted as a layout preserved text where columns are indicated with spaces.

                For example this:
                

                EDUCATION                                              SKILLS

                Higher Diploma Event Advertising                       Languages: English, Spanish
                University of Lytcotsglade, 2018                       People Management
                B.A. Event Management                                  Communication
                University of Lytcotsglade, 2009-2013                  Project Management
                
                should output:

                EDUCATION               

                Higher Diploma Event Advertising     
                University of Lytcotsglade, 2018           
                B.A. Event Management                   
                University of Lytcotsglade, 2009-2013         

                SKILLS
                Languages: English, Spanish
                People Management
                Communication
                Project Management

                """
            },
            {
                "role": "user", 
                
                "content": 
                f"""
                Take this text file and output the text in the correct reading order.
                {text_file}
                """
            }
        ]

        # Make request to chat model
        chat_response = chat_completion_request(messages, model=gpt_model)

        print(chat_response.json())

        response_content = chat_response.json()["choices"][0]["message"]["content"]

        output_file_path = os.path.join(output_dir, filename)

        # Write the response to the output text file
        with open(output_file_path, 'w') as output_file:
            output_file.write(response_content)


end_time = time.time()

print(f"Execution time: {end_time - start_time} seconds")
