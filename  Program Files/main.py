import os, sys
import openai

from dotenv import load_dotenv # Access things from .env file
load_dotenv()
openai.api_key = os.getenv('GPT-TOKEN')

# GPT TIME BABYYYYY WOOOOOOO
data_path = "../data"

"""
1. GET INFO FROM TXT FILES
"""