"""
Author: Raymond Xu
Date: January 10, 2025
"""
import level
import importance

def parse_major(courses_taken,major,college,major_data,course_data):
    if major == 'CS':
        if college == 'A&S':
            return parse_CS_CAS(courses_taken,major_data,course_data)

def parse_CS_CAS(courses_taken,major_data,course_data):
    data = major_data['A&S']
    result = {}
    section_names = ['Core','Math','CS Electives','Practicum or Project']
    for section in section_names:
        result[section] = {}
    result['Core']['Courses'] = data['Core']
    result['Core']['Description'] = None
    result['Core']['Number'] = None

    result['Math']['Courses'] = data['Math']
    result['Math']['Description'] = None
    result['Math']['Number'] = None

    # CS Electives
    cs_electives = level.data_level('CS',major_data,course_data,
    'A&S','CS Electives')
    cs_electives_sorted = importance.rank_importance(major_data,course_data,cs_electives,courses_taken,'A&S',"CS")
    result['CS Electives']['Courses'] = cs_electives_sorted
    result['CS Electives']['Description'] = data['CS Electives']['description']
    result['CS Electives']['Number'] = data['CS Electives']['number']

    # Practicum
    practicum = (level.find_CS4XX1(course_data) +
                data["Practicum or Project"]["included"])
    practicum_sorted = importance.rank_importance(major_data,course_data,practicum,courses_taken,'A&S',"CS")
    result["Practicum or Project"]['Courses'] = practicum_sorted
    result['Practicum or Project']['Description'] = data['Practicum or Project']['description']
    result['Practicum or Project']['Number'] = data['Practicum or Project']['number']


    return result
