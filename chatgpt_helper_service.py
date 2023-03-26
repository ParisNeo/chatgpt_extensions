from flask import Flask
from flask_cors import CORS
from blip_service import app as blip_app
from console_service import app as console_app

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "https://chat.openai.com"}})

# Register the routes of app1 and app2 with the main Flask application
app.register_blueprint(blip_app)
app.register_blueprint(console_app)

if __name__ == '__main__':
    app.run()