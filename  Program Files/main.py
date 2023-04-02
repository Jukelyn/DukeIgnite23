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

for course in list_courses: # Validate the courses one last time before using them...
    if course.valid() is False:
        sys.exit("Broken courses found. Investigate details...")

# Connect to the gpt api. The model we want is gpt-3.5-turbo
message_history = [
            {"role": "system", "content": "Your name is Classy and you're a class scheduling helper AI."},
            ]

while (True):
    # Get user input
    user_input = input("Enter query: ")
    if user_input == "":
        continue
    if user_input == "exit":
        break

    message_history.append({"role": "user", "content": user_input})
   
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message_history,
        max_tokens = 10000
    )

    message_history.append(response.choices[0].message)
    print("\n" + response.choices[0].message.content)

    if (response.choices[0].finish_reason != "stop"):
        print("\nYou've exceeded the max supply of tokens. Please restart the program.")
        break