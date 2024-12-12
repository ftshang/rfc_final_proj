# Required Software Dependencies:

- Python Version 3.9+
- Flask: ```pip install flask```
- Ollama: ```ollama run llama3.2``` , ```ollama run llama3.2-vision``` , ```ollama run qwen2.5-coder```

<b>IMPORTANT</b>: Make sure to change the ```FILE_DIR``` path in ```py.app``` to match the directory containing the images folder on your local machine. 

<b>Disclaimer:</b> Utilizing ```llama3.2-vision``` takes a lot of processing power that could stall your local machine. If the script takes too long to run, either change the model to ```llama3.2``` or skip using images. 

# Instructions on Running the Tool:
1. Open up ```index.html``` into your browser of choice.
2. Open up terminal, navigate to directory containing ```app.py```. Use ```py app.py``` to start the script.
3. Go back to the ```index.html``` page in your browser. Fill out RFC number field. Input the number of text-sections and image files you wish to use. Additional input fields will pop up after.
4. Paste in the RFC subsections within in text-section field.
5. For each image you wish to use, click on "Choose File" to locate the file within your local ```../images/``` folder.
6. Click "Generate Code" when fields have been filled out. The total duration will vary, but you can check the terminal of the Python script to see the current progress.
