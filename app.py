import requests
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent/'BLIP'))

import gradio as gr
import torch
from torchvision import transforms
from PIL import Image
import urllib.request
import io
from pathlib import Path

from BLIP.models.blip_vqa import blip_vqa

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
image_size = 384

class App():
    MODEL_URL = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_vqa.pth'
    MODELS_DIR = 'models'
    MODEL_FILENAME = 'blip_vqa.pth'    
    def __init__(self):
        self.selected_model=0
        self.check_model()
        
        # Load blip for question answer
        print("Loading Blip for question answering")
        model_url = str(Path(__file__).parent/'models/blip_vqa.pth')
        self.qa_model = blip_vqa(pretrained=model_url, image_size=image_size, vit='base', med_config = 'BLIP/configs/med_config.json')
        self.qa_model.eval()
        self.qa_model = self.qa_model.to(device)

        
        
        with gr.Blocks() as demo:
            gr.Markdown("# BLIP Image question and answer\nThis model allows you to ask questions about an image and get solid answers.\nIt can be used to caption images for stable diffusion fine tuning purposes or many other applications.\nBrought to gradio by @ParisNeo from the original github Blip code [https://github.com/salesforce/BLIP](https://github.com/salesforce/BLIP)\nThis model is described in this paper :[https://arxiv.org/abs/2201.12086](https://arxiv.org/abs/2201.12086)")
            with gr.Row():
                self.image_source = gr.inputs.Image(shape=(448, 448))
                with gr.Tabs():
                    with gr.Tab("Question/Answer"):
                        self.question = gr.inputs.Textbox(label="Custom question (if applicable)", default="Describe this image")
                        self.answer = gr.Button("Ask")
                        self.lbl_caption = gr.outputs.Label(label="Caption")
                        self.answer.click(self.answer_question_image, [self.image_source, self.question], self.lbl_caption)
        # Launch the interface
        demo.launch()
        
    def check_model(self):
        # Create the models directory if it doesn't exist
        Path(self.MODELS_DIR).mkdir(parents=True, exist_ok=True)

        # Check if the model file exists in the models directory
        model_filepath = Path(self.MODELS_DIR) / self.MODEL_FILENAME
        if not model_filepath.exists():
            # Download the model file from the URL
            response = requests.get(self.MODEL_URL)
            with open(model_filepath, 'wb') as f:
                f.write(response.content)  

    def answer_question_image(self, img, custom_question="Describe this image"):
        # Load the selected PyTorch model
        
        # Preprocess the image
        preprocess = transforms.Compose([
            transforms.Resize((image_size,image_size),interpolation=transforms.InterpolationMode.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ])
        img = preprocess(Image.fromarray(img.astype('uint8'), 'RGB'))
        
        # Make a prediction with the model
        with torch.no_grad():
            output = self.qa_model(img.unsqueeze(0).to(device), custom_question, train=False, inference='generate') 
            answer = output
        
        # Return the predicted label as a string
        return answer[0]

app = App()


