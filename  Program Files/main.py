import os, sys
import openai
from dotenv import load_dotenv # Access things from .env file

load_dotenv()
openai.api_key = os.getenv('GPT-TOKEN')