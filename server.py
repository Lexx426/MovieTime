from flask_app import app
from flask_app.controllers import user_controller
import os

from dotenv import load_dotenv
# load_dotenv()
# this is for creating an environmental variable , which is the API key in the .env file

if __name__ == "__main__":   
    load_dotenv()
    app.run(debug=True) 
    # print(os.environ['API_KEY'])