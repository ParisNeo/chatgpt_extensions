from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS, cross_origin

import requests
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent/'BLIP'))

from PIL import Image
import io
from pathlib import Path
import torch
from torchvision import transforms
from BLIP.models.blip_vqa import blip_vqa
import numpy as np
import re

import platform
import subprocess
import threading
import queue
import time



global output

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
image_size = 384

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "https://chat.openai.com"}})

encoding = 'ISO-8859-1'
# Define a global variable to store the output
output = ""

# Define a queue to store commands to be executed
command_queue = queue.Queue()

# Get the operating system
operating_system = platform.system()

# Execute the appropriate command based on the operating system
if operating_system == 'Windows':
    process = subprocess.Popen("powershell", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
elif operating_system == 'Darwin':  # macOS
    process = subprocess.Popen("/bin/bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
else:  # Linux or other Unix-like systems
    process = subprocess.Popen("/bin/bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



MODEL_URL = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_vqa.pth'
MODELS_DIR = 'models'
MODEL_FILENAME = 'blip_vqa.pth'

def check_model():
    # Create the models directory if it doesn't exist
    Path(MODELS_DIR).mkdir(parents=True, exist_ok=True)

    # Check if the model file exists in the models directory
    model_filepath = Path(MODELS_DIR) / MODEL_FILENAME
    if not model_filepath.exists():
        # Download the model file from the URL
        response = requests.get(MODEL_URL)
        with open(model_filepath, 'wb') as f:
            f.write(response.content)  

print("Checking model ...")
check_model()
print("Ok")

# Load blip for question answer
print("Loading Blip for question answering...",end="")
model_url = str(Path(__file__).parent/'models/blip_vqa.pth')
qa_model = blip_vqa(pretrained=model_url, image_size=image_size, vit='base', med_config = 'BLIP/configs/med_config.json')
qa_model.eval()
qa_model = qa_model.to(device)
print("OK")

blip_dict={"image":None,"Questions":[]}

@app.route('/set_image', methods=['POST'])
@cross_origin()
def set_image():
    image_file = request.files['image']
    if image_file:
        file_path = './image.png'
        image_file.save(file_path)
        with open(file_path, 'rb') as f:
            img_bytes = f.read()
        
        # Load the image using Pillow
        img = Image.open(io.BytesIO(img_bytes))
        blip_dict["image"]=img
        print("File saved. Ready to answer questions")
        # Process the file path
        response = make_response("File path received!")
        return response
    else:
        response = make_response("File path missing!")
        return response


@app.route('/question', methods=['POST'])
@cross_origin()
def question():
    # initializing replace string
    repl = ""
    
    # initializing substring to be replaced
    subs = "can you"
    compiled = re.compile(re.escape(subs), re.IGNORECASE)
    questions = request.json.get('questions')
    print(f"Received {questions}")
    blip_dict["Questions"]=questions
    
    preprocess = transforms.Compose([
        transforms.Resize((image_size,image_size),interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
    ])

    img = preprocess(blip_dict["image"])
    
    # Make a prediction with the model
    answers = []
    with torch.no_grad():
        for question in questions:
            question = compiled.sub(repl, question).strip()
            print(f'Asking question :{question}')
            output = qa_model(img.unsqueeze(0).to(device), question, train=False, inference='generate') 
            answers.append(output[0])
    

    # Create a JSON response with the processed data
    response = {
        'status':'success',
        'answers':answers
    }

    return jsonify(response)


# Define a function to run a command on the console
def run_command(command):
    global output
    
    print(f"process : {process}")
    print(f"process stdin : {process.stdin}")
    while process.stdin is None:
        time.sleep(0.1)    
    # Send the command to the console
    process.stdin.write(command.encode(encoding) + b"\n")
    process.stdin.flush()
    
    # Wait for the output to be generated
    time.sleep(1.0)

run_command("cd ~\Documents\chatgpt_extensions")


def watch_output():
    global output
    print("Running output watcher")
    while True:
        # Read the output of the console and add it to the global variable
        stdout = process.stdout.readline().decode(encoding)
        if stdout:
            output += stdout
            print(stdout.strip())


# Define a function to execute the queued commands
def execute_commands():
    global output
    while True:
        command = command_queue.get()
        try:
            print(f"Executing command {command}")
            run_command(command)
            print(f"Command {command} executed")
        except Exception as ex:
            output += str(ex)
        command_queue.task_done()
        print(f"Waiting for next command")

# Start the thread to watch the console output
output_thread = threading.Thread(target=watch_output)
output_thread.daemon = True
output_thread.start()

# Start the thread to execute commands
execute_thread = threading.Thread(target=execute_commands)
execute_thread.daemon = True
execute_thread.start()

# Define the route to receive commands from the frontend
@app.route('/command', methods=['POST'])
def execute_command():
    global output
    command = request.json['command']
    print(f"Received command : {command}")

    # Add the command to the queue
    command_queue.put(command)

    print(f"Entries in queue : {command_queue.qsize()}")
    # Wait for a short period of time to allow the output to be captured
    time.sleep(1)

    # Send any pending stdout and stderr data
    output_lines = output.split('\n')
    output = ""
    return jsonify(output=output_lines)

@app.route('/console')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
