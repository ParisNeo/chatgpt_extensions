from flask import Flask, request, jsonify, make_response
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

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
image_size = 384

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "https://chat.openai.com"}})


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
print("Loading Blip for question answering")
model_url = str(Path(__file__).parent/'models/blip_vqa.pth')
qa_model = blip_vqa(pretrained=model_url, image_size=image_size, vit='base', med_config = 'BLIP/configs/med_config.json')
qa_model.eval()
qa_model = qa_model.to(device)

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

if __name__ == '__main__':
    app.run(debug=True)
