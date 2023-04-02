# This script is meant to be ran once, it takes quite some time to go through and make many API calls and then gets the data
# to place into txt files to access much faster, later.

import time # Timing
start_time = time.time()

import os, sys
from dotenv import load_dotenv # Access things from .env file

import requests # API interactions
import Course # Used to create course objects

load_dotenv()
api_token = os.getenv('TOKEN')
base_url = "https://streamer.oit.duke.edu/curriculum/"
data_path = "../"

if os.path.exists("Courses.txt"):
    os.remove("Courses.txt")
else:
    print("Starting...")

# Get a list of subjects
def getListSubjects():
    """
    Gets a list of the subjects
    """
    list_subjects_raw = requests.get(f"{base_url}list_of_values/fieldname/SUBJECT?access_token={api_token}")
    if list_subjects_raw.status_code != 200:
        sys.exit(f"L + Error accessing API. gg, go next.\nStatus code: {list_subjects_raw.status_code}")
    list_subjects_json = list_subjects_raw.json() # Response to JSON
    return list_subjects_json["scc_lov_resp"]["lovs"]["lov"]["values"]["value"] # Unpacking

list_subjects = getListSubjects()

def getSubjectCodes(subjects):
    """
    Loop thru subjects to get the codes and store them
    """
    res = []
    for i in range(len(subjects)):
        res.append(subjects[i]["code"])
    return res

list_subject_codes = getSubjectCodes(list_subjects)

with open(f"{data_path}data/CourseCodes.txt", "w") as txt_file:
    for codes in list_subject_codes:
        txt_file.write("".join(codes) + "\n")

def getCourseList(code):
    """
    Gets the list of all the courses from each subject and make each of them into objects
    """
    raw = requests.get(f"{base_url}courses/subject/{code}?access_token={api_token}")
    return raw.json() # Response to JSON

list_course_objs = []
for code in list_subject_codes:
    list_courses = getCourseList(code)
    
    if len(list_courses) == 0: # should only happen if the GET is messed up... not sure why I'm keeping this here but oh well
        sys.exit("er0r. git gud kid... if this happened then something went wayyy wrong... gg")

    # For some reason they have these named weirdly, don't focus too much on the names of the keys here...
    tmp = list_courses["ssr_get_courses_resp"]["course_search_result"] # Unpacking a bit
    if int(tmp["ssr_crs_srch_count"]) <= 3: # There are no courses for this subject so we just skip this subject enitrely
        continue

    list_courses = tmp["subjects"]["subject"]["course_summaries"]["course_summary"] # Unpacking the courses
    print(f"\nRunning time: {round(time.time() - start_time, 3)}s")
    print(f"Current subject: {code}")
    numCourses = len(list_courses)
    print(f"Courses in subject: {numCourses}\n")

    for i in range(numCourses): # Loop thru the courses to make Course objects
        if list_courses[i]['ssr_crse_typoff_cd'] is None: # If the course isn't offered just skip it
            continue
        if "OCCASIONAL" in list_courses[i]['ssr_crse_typoff_cd']:
            continue

        subject_desc = list_courses[i]['subject_lov_descr']
        if "(Taught at " in subject_desc: # If the course is not taught AT DUKE, just skip it. These courses have "(Taught at X)" 
            continue
        
        crseId = list_courses[i]['crse_id']
        subject = list_courses[i]['subject']
        title = list_courses[i]['course_title_long']
        offering = list_courses[i]['ssr_crse_typoff_cd'] # if None, just throw out, as it's not offered.
        subjectLine = f"{subject} - {subject_desc}"
        
        print(f"Working on course: {crseId} ({i} of {numCourses})...")

        # Lookup course for the course desc
        tmp = requests.get(f"{base_url}courses/crse_id/{crseId}/crse_offer_nbr/1?access_token={api_token}")
        tmp_json = tmp.json()
        try:
            if tmp_json["error"]:
                continue
        except KeyError:
            pass

        tmp1 = tmp_json["ssr_get_course_offering_resp"]["course_offering_result"]
        if int(tmp1["ssr_terms_offered_count"]) == 0:
            continue
        courseDesc = tmp1["course_offering"]["descrlong"]
        
        with open(f"{data_path}data/Courses.txt", "a") as txtFile: # Append
            txtFile.write(f"{subjectLine} | {title} | {crseId} | {courseDesc} | {offering}\n") # Format

        currCourse = Course.Course(subjectLine, title, crseId, courseDesc, offering) # Current course
        list_course_objs.append(currCourse) # Add to list

# print(len(list_course_objs))