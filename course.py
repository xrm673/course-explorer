"""
Author: Raymond Xu
Start Date: December 20, 2024
"""

import re
import special

NEXT_SEMESTER = "SP25"

def contain_course(course_data,course_code):
    subject = get_subject(course_code)
    if subject in course_data and course_code in course_data[subject]:
        return True
    else:
        print(f"{course_code} has not been offered by Cornell for three years")
        return False

# helper for match_level
def get_subject(course_code):
    """
    return a str that indicates the subject of a course
    """
    letter = re.search(r'[A-Za-z]+', course_code)
    assert letter
    subject = letter.group(0)
    return subject

def get_number(course_code):
    number = re.search(r'\d+', course_code)
    assert number
    course_number = number.group(0)
    return course_number

# helper for match_level
def get_level(course_code):
    """
    return an int that indicates the level of the course
    """
    course_number = get_number(course_code)
    level = int(course_number[0])
    return level

def get_semester_offered(course_code,course_data):
    subject = get_subject(course_code)
    return course_data[subject][course_code]["Semester Offered"]

def available_next_semester(course_code,course_data):
    semesters = get_semester_offered(course_code,course_data)
    if semesters[0] == NEXT_SEMESTER:
        return True
    return False

def get_prereq(course_data,course_code):
    subject = get_subject(course_code)
    if contain_course(course_data,course_code):
        prereq = course_data[subject][course_code]["Prerequisites"]
        return prereq
    else:
        return None

def get_coreq(course_data,course_code):
    subject = get_subject(course_code)
    if contain_course(course_data,course_code):
        coreq = course_data[subject][course_code]["Corequisites"]
        return coreq
    else:
        return None

def get_all_prereq(self):
    """
    Return a list of Course objects in topological order.

    For example, if self is CS3110 and its prereq is CS2110, the method
    will check the prereq of CS2110 (which is CS1110) and return
    [CS1110, CS2110, CS3110]
    """
    pass

#eligibility
def check_eligibility(course_data,courses_taken,course_code):
    """
    return true if the course is eligible to take
    """
    if course_is_special(course_code):
        return special.special_eligibility(courses_taken,course_code)
    subject = get_subject(course_code)
    prereq = get_prereq(course_data,course_code)
    coreq = get_coreq(course_data,course_code)
    prereq_not_fulfilled = []
    coreq_not_fulfilled = []
    if prereq:
        prereq_not_fulfilled = not_fulfilled_2dlist(courses_taken,prereq)
    if coreq:
        for group in coreq:
            fulfilled = False
            for coreq_course in group:
                coreq_requirement = get_prereq(course_data,coreq_course)
                if not coreq_requirement:
                    fulfilled = True
                    break
                coreq_not_fulfilled_sub = not_fulfilled_2dlist(courses_taken,coreq_requirement)
                if coreq_not_fulfilled_sub == []:
                    fulfilled = True
                    break
            if not fulfilled:
                coreq_not_fulfilled += coreq_not_fulfilled_sub
    if prereq_not_fulfilled == [] and coreq_not_fulfilled == []:
        return True,[]
    return False,prereq_not_fulfilled + coreq_not_fulfilled

# helper for check_eligibility
def not_fulfilled_2dlist(courses_taken,requirement):
    """
    return a 2d list of required courses that have not been completed

    Parameter courses_taken: courses that have already been taken
    Precondition: a list of course codes
    """
    if requirement == []:
        return []

    result = []
    for sublist in requirement:
        fulfilled = False
        for course in courses_taken:
            if course in sublist:
                fulfilled = True
                break
        if not fulfilled:
            result.append(sublist)

    return result

# helper for check_eligibility
def course_is_special(course_code):
    if course_code in ["CS4744","CS5775","MATH4030","INFO3140","INFO3152",
    "INFO4152","INFO5152","CS4210","CS4745"]:
        return True
    return False


def semester_provided(self,next_semester):
    """
    Return a str showing which semester the course is likely provided


    For case the schedule of next semester is released:

    If the course is listed in the schedule, return "Provided in
    {next_semester}".

    If the course is not listed in the schedule, and it is not provided for
    three years, return "Not provided for three years"

    If the course is not listed in the schedule, while it's only provided in
    the "opposite semester" in past three years, return "Likely provided in
    {next_next_semester}". For example, if the next_semester is "SP25" and
    the course is only provided in fall semesters in the last three years,
    return "Likely provided in FA25"

    If the course is not listed in the schedule, while it specifies that it
    will be provided in the "opposite semester" in its course description,
    return "Likely provided in {next_next_semester}"

    Else, return "Not provided in {next_semester}"


    For case the schedule of next semester is NOT yet released:

    If the course is provided in every fall and spring semester in the past
    three years, return "Likely provided in {next_semester}."

    If the course is only provided in every fall semester in the past three
    years, return "Likely provided in {next_fall_semester}." Same for spring.

    If the course is not provided for three years, return "Not provided for
    three years".

    Else, return "Unknown".

    Parameter next_semester: the next semester of current time
    Precondition: a str in form of season + year, such as "SP25". Season
    must be FA or SP.
    """
    pass

def lec_time_overlap(self,another_course,semester):
    """
    Return True if there is an overlap in lecture time between self and
    another_course in the given semester, return False otherwise

    Parameter another_course: the course to compare with
    Precondition: another_course is a Course object that is provided in the
    given semester

    Parameter semester: the semester of comparison
    Precondition: semester is a Semester object that has both self and
    another_course
    """
    pass
