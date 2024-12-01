# import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for local testing

FILE_DIR = 'C:/Users/tatao/Desktop/final_proj_test/state_diagrams/'

@app.route("/generate", methods=["POST"])
def generate_response():
    data = request.get_json()
    rfcNumber = data.get("rfcNumber")
    sections = data.get("sections")
    files = data.get("files")

    # if not prompt:
    #     return jsonify({"response": "No prompt provided"}), 400


    # 1.) Get a general "skeleton specification" from Llama3.2:
    prompt = 'Provide the specifications in bullet points for RFC ' + rfcNumber + ':\n'

    response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': prompt
        },
    ])

    print("Prompt: ", prompt)
    print("===================================")
    print(response['message']['content'])
    print("===================================")

    # 2.) Process the Sections
    for section in sections:
        if section == "":
            continue
        prompt = "Update the specification to keep its content:\n" + response['message']['content'] + "\nbut add helpful information from the following portion of RFC " + rfcNumber + ":\n" + section
        response = ollama.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        print("Prompt:", prompt)
        print("===================================")
        print(response['message']['content'])
        print("===================================")

    # 3.) Process the Files with llama3.2-vision



    # 4.) Feed into llama3.1 for final specification
    prompt = "Revise the following RFC " + rfcNumber + " specification to bullet points that list out the steps of the protocol: \n" + response['message']['content']
    print("Prompt", prompt)
    response = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ])
    print("===================================")
    print(response['message']['content'])
    print("===================================")

    # 5.) Use qwen2.5-code to turn specification into psuedocode
    prompt = "Turn the following RFC " + rfcNumber + " specification into Python pseudocode: \n" + response['message']['content']
    print("Prompt", prompt)
    response = ollama.chat(model='qwen2.5-coder', messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ])
    print("===================================")
    print(response['message']['content'])
    print("===================================")

    # 6.) Use qwen2.5-code to turn pseudocode into Python code
    prompt = "Turn the following psuedocode for RFC " + rfcNumber + " to Python code: \n" + response['message']['content']
    print("Prompt", prompt)
    response = ollama.chat(model='qwen2.5-coder', messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ])

    print("===================================")
    print(response['message']['content'])
    print("===================================")

    return jsonify({"response": response['message']['content']})

if __name__ == "__main__":
    app.run(port=5000)
