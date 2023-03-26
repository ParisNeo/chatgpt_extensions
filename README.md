# ChatGpt-Extensions

ChatGpt-Extensions is a set of services using Flask server that allow chatgpt-personality-selector to give chatgpt access to other tools like BLIP and Stable diffusion.

Here are the extensions
## ChatGpt-Blip

ChatGpt-Blip is a web application that allows users to interact with two AI models: ChatGpt and BLIP. ChatGpt is a large language model trained by OpenAI, while BLIP is a local image question-answering system.

### Installation

To use ChatGpt-Blip, you need to perform the following steps:

1. Install the ChatGpt-Blip Google Chrome extension from the [Chrome Web Store](https://chrome.google.com/webstore/detail/chatgpt-personality-selec/jdmpccdlifdkhniemenfmieffkdblahk?hl=fr&authuser=0). This extension hooks into the ChatGpt web interface to condition ChatGpt to be one of many personalities, and allows ChatGpt to communicate with BLIP since V2.6.0.

2. Clone the ChatGpt-Blip repository from GitHub:
```
git clone https://github.com/ParisNeo/chatgpt_extensions.git
```

3. Clone the BLIP submodule:

```
cd chatgpt_extensions
git submodule update --init --recursive
```

4. Install the required libraries:

```
pip install -r requirements.txt
```


Note that you need to have Python 3.7 or higher installed.

### Usage

To use ChatGpt-Blip, follow these steps:

1. Start the Flask server:

```
python app.py
```

This will start a local server that can receive an image and a bunch of questions about the image, and then answer them.

2. Open a webpage with ChatGpt loaded and the ChatGpt-Personality-Selector extension enabled.

3. In the Personality settings ui, select the language, in categories, select Image Enabled ChatGPT, in personality select Image understanding, then select the image you want to describe and hit Apply personality.

4. Now just wait and watch the two AI talking to each other until chatgpt ends the discussion saying VERDICT and shows you its description of the image.

5. At the end, ChatGpt will describe the image in detail.

## Acknowledgements

ChatGpt-Blip is based on two AI models: ChatGpt by OpenAI and BLIP by Junnan Li
et al.

## License

This software is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

