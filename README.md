# Chat GPT Extensions

ChatGpt-Extensions is a set of services using Flask server that allow chatgpt-personality-selector to give chatgpt access to other tools like BLIP and Stable diffusion.

## Installation

To install the application, follow these steps:

1. Clone the repository: `git clone https://github.com/ParisNeo/chatgpt_extensions`
2. Navigate to the project directory: `cd chatgpt_extensions`
3. Run the installation script: `install.bat` (Windows) or `install.sh` (Linux/macOS). If you don't have a cuda capable device or, you may install the cpu version using `install_cpu.bat` (Windows) or `install_cpu.sh` (Linux/macOS). 

This will donwload and install pytorch and all required modules (such as BLIP) 
## Usage


To launch the application, run the appropriate launch script for your operating system:

- Windows: `run.bat`
- Linux/macOS: `./run.sh`

```sh

# Launch the application
./run.sh  # Linux/macOS
run.bat  # Windows

```

This will automatically activate the virtual environment and launch the application.

## Dependencies
This application requires the following dependencies:

- Python 3.7 or higher



# Sub applications


Here are the extensions
## ChatGpt-Blip

ChatGpt-Blip is a web application that allows users to interact with two AI models: ChatGpt and BLIP. ChatGpt is a large language model trained by OpenAI, while BLIP is a local image question-answering system.


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

# Contributing
To contribute to this project, follow these steps:

1. Fork the repository
2. Create a new branch: git checkout -b my-feature-branch
3. Make changes and commit them: git commit -am 'Add new feature'
4. Push your changes to your fork: git push origin my-feature-branch
5. Open a pull request on the original repository

## License

This software is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

