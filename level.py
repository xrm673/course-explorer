"""
Author: Raymond Xu
Start Date: January 10, 2025
"""

import course

def level_required(course_data,courses_taken,subject,min_level,min_credit,
number,excluded=[],included=[]):
    """
    return the courses that have fulfilled the level requirement and the courses
    that can be used to fulfill the requirement. If the requirement has been
    fulfilled, the second list is empty
    """
    fulfilled = level_taken(course_data,courses_taken,subject,min_level,min_credit,excluded,included)
    not_fulfilled = []
    if len(fulfilled_courses) >= number:
        return fulfilled,not_fulfilled
    for course in level(course_data,subject,min_level,min_credit,excluded,included):
        if not course in fulfilled:
            not_fulfilled.append(course)
    return fulfilled,not_fulfilled

def data_level(subject,major_data,course_data,college,category):
    min_level = major_data[college][category]["min_level"]
    included = major_data[college][category]["included"]
    excluded = major_data[college][category]["excluded"]
    min_credit = major_data[college][category]["min_credit"]
    return level(course_data,subject,min_level,min_credit,excluded,included)

# helper for level_required,
def level(course_data,subject,min_level,min_credit,excluded=[],included=[]):
    """
    return a list with all courses that meet the level requirement in a subject
    """
    result = []
    for course_code in course_data[subject]:
        if match_level(course_data,course_code,subject,min_level,min_credit,excluded,included):
            result.append(course_code)
    result = result + included
    return result

# helper for level_required
def level_taken(course_data,courses_taken,subject,min_level,min_credit,excluded=[],included=[]):
    """
    return a list of courses taken that fulfilled the level requirement
    """
    result = []
    for course_code in courses_taken:
        if level.match_level(course_data,course_code,subject,min_level,min_credit,excluded,included):
            result.append(course_code)
    return result

def data_match_level(course_data,major_data,course_code,college,subject,category):
    """
    return true if the course match the level requirement of a subject
    """
    min_level = major_data[college][category]["min_level"]
    included = major_data[college][category]["included"]
    excluded = major_data[college][category]["excluded"]
    min_credit = major_data[college][category]["min_credit"]
    return match_level(course_data,course_code,subject,min_level,min_credit,excluded,included)

# helper for app.level, app.level_taken
# helper for majorImportance.match_level_requirement
def match_level(course_data,course_code,subject,min_level,min_credit,
excluded=[],included=[]):
    """
    return true if the course match the level requirement of a subject
    """
    if course_code in included:
        return True
    if course_code in excluded:
        return False
    if (course.get_subject(course_code) == subject
    and course.get_level(course_code) >= min_level):
        course_max = course.get_max_credit(course_data,course_code)
        if course_max and (course_max >= min_credit):
            return True
    return False

def data_only_level(course_data,major_data,college,subject,category):
    level = major_data[college][category]["level"]
    included = major_data[college][category]["included"]
    excluded = major_data[college][category]["excluded"]
    min_credit = major_data[college][category]["min_credit"]
    return only_level(course_data,subject,level,min_credit,excluded,included)

def only_level(course_data,subject,level,min_credit,excluded=[],included=[]):
    result = []
    for course_code in course_data[subject]:
        if ((not course_code in excluded) and
        (course.get_level(course_code) == level) and
        (course.get_max_credit(course_data,course_code) >= min_credit)):
            result.append(course_code)
    result = result + included
    return result



def find_CS4XX1(course_data):
    result = []
    for course_code in course_data['CS']:
        if course.get_level(course_code) == 4 and course_code[-1] == "1":
            result.append(course_code)
    return result
