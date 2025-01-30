"""
Author: Raymond Xu
Start Date: January 19, 2025
"""
import os
import json

def open_raw_data():
    with open('data/course_data/combined/combined.json', 'r') as file:
        course_data = json.load(file)
    return course_data

def correct(course_data):
    correct_cs(course_data)
    correct_econ(course_data)
    correct_math(course_data)

def correct_cs(course_data):
    data = course_data["CS"]

    if (
    "excellent performance in CS 1110, CS 1112 or equivalent course in "
    "Java or C++, or permission of instructor"
    ) in data["CS2112"]["Specific Requirements"]:
        data["CS2112"]["Prerequisites"] = [["CS1110","CS1112"]]

    if (
    "CS 3110 or permission of instructor. Students are expected to be "
    "proficient with programming (e.g. CS 2110), and proof (e.g. CS 2800 or a "
    "mathematics course numbered 3000 or above)."
    ) in data["CS4160"]["Specific Requirements"]:
        data["CS4160"]["Prerequisites"] = [["CS3110"],["CS2800"]]
        data["CS5160"]["Prerequisites"] = [["CS3110"],["CS2800"]]

    data["CS3110"]["Prerequisites or Corequisites"] = []

    course_data["CS"] = data

def correct_econ(course_data):
    data = course_data["ECON"]

    if (
    "Prerequisite: ECON 1110. Recommended Prerequisite: ECON 1120."
    ) in data["ECON2300"]["Specific Requirements"]:
        data["ECON2300"]["Prerequisites"] = [["ECON1110"]]

    if (
    "Prerequisite: ECON 1110, ECON 1120 and ECON 3040, or equivalents."
    ) in data["ECON4210"]["Specific Requirements"]:
        data["ECON4210"]["Prerequisites"] = [["ECON1110"],["ECON1120"],["ECON3040"]]

    course_data["ECON"] = data

def correct_math(course_data):
    data = course_data["MATH"]

    if (
    "three years of high school mathematics (including trigonometry and "
    "logarithms) or a precalculus course (e.g., MATH 1101). MATH 1110 can serve"
    " as a one-semester introduction to calculus or as part of a two-semester "
    "sequence in which it is followed by MATH 1120. For guidance in selecting "
    "an appropriate course, please consult First Steps in Math."
    ) in data["MATH1110"]["Specific Requirements"]:
        data["MATH1110"]["Prerequisites"] = []

    course_data["MATH"] = data

def output_data(course_data):
    with open('data/course_data/combined/corrected.json' , 'w') as json_file:
        json.dump(course_data,json_file,indent=4)

course_data = open_raw_data()
correct(course_data)
output_data(course_data)
