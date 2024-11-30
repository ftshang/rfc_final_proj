# import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for local testing

@app.route("/generate", methods=["POST"])
def generate_response():
    data = request.get_json()
    prompt = data.get("prompt")

    print("is this working?")
    print(data)

    if not prompt:
        return jsonify({"response": "No prompt provided"}), 400

    response = ollama.chat(model='llama3.1', messages=[
    {
        'role': 'user',
        'content': 'Provide me with Python code that implements the Tower of Hanoi.',
    },
    ])

    print(response['message']['content'])

    return jsonify({"response": response['message']['content']})

if __name__ == "__main__":
    app.run(port=5000)
