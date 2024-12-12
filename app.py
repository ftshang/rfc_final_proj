from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)

# IMPORTANT: Update FILE_DIR with the full directory path that points to the images folder on your local machine.
FILE_DIR = 'C:/Users/tatao/Desktop/final_proj/images/'

@app.route("/generate", methods=["POST"])
def generate_response():
    data = request.get_json()
    rfcNumber = data.get("rfcNumber")
    sections = data.get("sections")
    files = data.get("files")
    prompt_number = 1

    # 1.) Get a general "skeleton specification" from Llama3.2:
    prompt = 'Provide the specifications in bullet points for RFC ' + rfcNumber + '.'
    print("Prompt #" + str(prompt_number) + ":\n" + prompt)
    print("===================================")
    response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': prompt
        },
    ])
    print("Response to Prompt #" + str(prompt_number) + ":\n" + response['message']['content'])
    print("===================================")
    prompt_number += 1

    # 2.) Process the Sections
    for section in sections:
        if section == "":
            continue
        prompt = "The first block of text is a bullet point specification for RFC " + rfcNumber + ". The second block of text is a portion of technical documentation from RFC " + rfcNumber + ". Update the bullet point specification (first block of text) according to the second block of technical documentation.\n"
        prompt += "\n\n" + response['message']['content'] + "\n\n"
        prompt += "\n" + section

        print("Prompt #" + str(prompt_number) + ":\n" + prompt)
        print("===================================")
        response = ollama.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        print("Response to Prompt #" + str(prompt_number) + ":\n" + response['message']['content'])
        print("===================================")
        prompt_number += 1

    # 3.) Process the Files with llama3.2-vision
    vision_prompt_num = 1
    for file_path in files:
        vision_prompt = 'Analyze this file. Give me specific bullet points explaining this diagram.'
        print("Vision Prompt #" + str(vision_prompt_num) + ":\n" + "File Name: " + file_path + "\n" + vision_prompt)
        print("===================================")
        vision_response = ollama.chat(model="llama3.2-vision", messages=[
            {
                'role': 'user',
                'content': vision_prompt,
                'images': [FILE_DIR + file_path]
            }
        ])
        print("Response to Vision Prompt #" + str(vision_prompt_num) + ":\n" + vision_response['message']['content'])
        print("===================================")

        prompt = "The first block of text is a bullet point specification for RFC " + rfcNumber + ". The second block of text describes the diagrams from RFC " + rfcNumber + ". Update the bullet point specification (first block of text) according to the second block of technical documentation.\n"
        prompt += "\n\n" + response["message"]["content"] + "\n\n"
        prompt += "\n" + vision_response["message"]["content"]
        print("Prompt #" + str(prompt_number) + ":\n" + prompt)
        print("===================================")
        response = ollama.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        print("Response to Prompt #" + str(prompt_number) + ":\n" + response['message']['content'])
        print("===================================")
        vision_prompt_num += 1
        prompt_number += 1

    # 4.) Feed into llama3.1 for final specification
    prompt = "Revise the following RFC " + rfcNumber + " specification to bullet points that list out the steps of the protocol: \n\n" + response['message']['content']
    print("Prompt #" + str(prompt_number) + ":\n" + prompt)
    print("===================================")
    response = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ])
    print("Response to Prompt #" + str(prompt_number) + ":\n" + response['message']['content'])
    print("===================================")
    prompt_number += 1

    # 5.) Use qwen2.5-code to turn specification into psuedocode
    prompt = "Turn the following RFC " + rfcNumber + " specification into pseudocode, explaining each step of the algorithm: \n\n" + response['message']['content']
    print("Prompt #" + str(prompt_number) + ":\n" + prompt)
    print("===================================")
    response = ollama.chat(model='qwen2.5-coder', messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ])
    print("Response to Prompt #" + str(prompt_number) + ":\n" + response['message']['content'])
    print("===================================")
    prompt_number += 1

    # 6.) Use qwen2.5-code to turn pseudocode into Python code
    prompt = "Turn the following psuedocode for RFC " + rfcNumber + " to Python code: \n\n" + response['message']['content']
    print("Prompt #" + str(prompt_number) + ":\n" + prompt)
    print("===================================")
    response = ollama.chat(model='qwen2.5-coder', messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ])
    print("Response to Prompt #" + str(prompt_number) + ":\n" + response['message']['content'])
    print("===================================")

    return jsonify({"response": response['message']['content']})

if __name__ == "__main__":
    app.run(port=5000)
