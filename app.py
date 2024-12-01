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
    terminology = data.get("terminology")
    overview = data.get("overview")
    specification = data.get("specification")
    stateDiagram = data.get("stateDiagram")

    print("is this working?")
    print(data)

    # if not prompt:
    #     return jsonify({"response": "No prompt provided"}), 400


    rfc_prompt = 'Provide the specifications in bullet points for RFC ' + rfcNumber + ':\n'

    first_response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': rfc_prompt
        },
    ])

    print(first_response['message']['content'])

    terminology_prompt = 'Update the current response: ' + first_response['message']['content'] + "with the following: \n" + terminology

    second_response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': terminology_prompt
        },
    ])

    print(second_response['message']['content'])
    # response_psuedocode = ollama.chat(model='llama3.2', messages=[
    # {
    #     'role': 'user',
    #     'content': new_str + prompt,
    # },
    # ])

    # print(response['message']['content'])

    return jsonify({"response": second_response['message']['content']})

if __name__ == "__main__":
    app.run(port=5000)
