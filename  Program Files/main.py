import os, sys
import openai
import Course

from dotenv import load_dotenv # Access things from .env file
load_dotenv()
openai.api_key = os.getenv('GPT-TOKEN')

# GPT TIME BABYYYYY WOOOOOOO
data_path = "../data"

list_courses = []
with open(f"{data_path}/Courses.txt", "r") as f: # Read in the data
    for courseData in f: # Create Coures objects from the data and append
        pieces_raw = courseData.split('|') # List of the pieces
        pieces = [s.strip() for s in pieces_raw]
        #print(pieces)
        currCourse = Course.Course(pieces[0], pieces[1], pieces[2], pieces[3], pieces[4])
        list_courses.append(currCourse)

for course in list_courses:
    if course.valid() is False:
        sys.exit("Broken courses found. Investigate details...")