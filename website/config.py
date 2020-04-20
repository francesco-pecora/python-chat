import os
from dotenv import load_dotenv
from pathlib import Path

# load enviromental variables
evn_path = Path(".") / ".env"
load_dotenv(dotenv_path=evn_path)

class Config:
    TESTING = os.getenv("TESTING")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SERVER = os.getenv("SERVER")