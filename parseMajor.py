"""
Author: Raymond Xu
Date: January 10, 2025
"""
import level
import importance
import course

def parse_major(course_data,courses_taken,college,major_displayed,major_d_data,
major_left=None,major_l_data=None,minor1=None,minor1_data=None,minor2=None,
minor2_data=None,minor3=None,minor3_data=None):
    if college == 'A&S':
        if major_displayed == 'ARTH':
            return parse_ARTH_CAS(course_data,courses_taken,major_d_data,
            major_left,major_l_data,minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
        if major_displayed == "ECON":
            return parse_ECON_CAS(course_data,courses_taken,major_d_data,
            major_left,major_l_data,minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
        if major_displayed == 'CS':
            return parse_CS_CAS(course_data,courses_taken,major_d_data,
            major_left,major_l_data,minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
        if major_displayed == 'INFO':
            return parse_INFO_CAS(course_data,courses_taken,major_d_data,
            major_left,major_l_data,minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)

def parse_ARTH_CAS(course_data,courses_taken,major_d_data,major_left=None,
major_l_data=None,minor1=None,minor1_data=None,minor2=None,minor2_data=None,minor3=None,minor3_data=None):
    data = major_d_data['A&S']
    result = {}
    section_names = ['Core Courses','2000 Level','3000 Level','4000 Level',
    '3000+']
    for section in section_names:
        result[section] = {}

    taken_fulfilled = []

    result['Core Courses']['Courses'] = data['Core Courses']
    result['Core Courses']['Description'] = None
    result['Core Courses']['Number'] = None
    core_taken = course.fulfilled_2dlist(courses_taken,data['Core Courses'])
    taken_fulfilled += core_taken

    level2000 = level.data_only_level(course_data,major_d_data,"A&S","ARTH",
    '2000 Level')
    level2000_sorted = importance.rank_importance(major_d_data,course_data,
    level2000,courses_taken,'A&S',"ARTH",major_left,major_l_data,
    minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
    result['2000 Level']['Courses'] = level2000_sorted
    result['2000 Level']['Description'] = None
    result['2000 Level']['Number'] = data['2000 Level']['number']

    level3000 = level.data_only_level(course_data,major_d_data,"A&S","ARTH",
    '3000 Level')
    level3000_sorted = importance.rank_importance(major_d_data,course_data,
    level3000,courses_taken,'A&S',"ARTH",major_left,major_l_data,
    minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
    result['3000 Level']['Courses'] = level3000_sorted
    result['3000 Level']['Description'] = None
    result['3000 Level']['Number'] = data['3000 Level']['number']

    level4000 = level.data_only_level(course_data,major_d_data,"A&S","ARTH",
    '4000 Level')
    level4000_sorted = importance.rank_importance(major_d_data,course_data,
    level4000,courses_taken,'A&S',"ARTH",major_left,major_l_data,
    minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
    result['4000 Level']['Courses'] = level4000_sorted
    result['4000 Level']['Description'] = None
    result['4000 Level']['Number'] = data['4000 Level']['number']

    level3000_more = level.data_level("ARTH",major_d_data,course_data,"A&S",
    '3000+')
    level3000_more_sorted = importance.rank_importance(major_d_data,course_data,
    level3000_more,courses_taken,'A&S',"ARTH",major_left,major_l_data,
    minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
    result['3000+']['Courses'] = level3000_more_sorted
    result['3000+']['Description'] = None
    result['3000+']['Number'] = data['3000+']['number']

    return result

def parse_ECON_CAS(course_data,courses_taken,major_d_data,major_left=None,
major_l_data=None,minor1=None,minor1_data=None,minor2=None,minor2_data=None,minor3=None,minor3_data=None):
    data = major_d_data["A&S"]
    result = {}
    section_names = ['Basics','Core Courses','Electives']
    for section in section_names:
        result[section] = {}
    result['Basics']['Courses'] = data['Basics']
    result['Basics']['Description'] = None
    result['Basics']['Number'] = None

    result['Core Courses']['Courses'] = data['Core Courses']
    result['Core Courses']['Description'] = None
    result['Core Courses']['Number'] = None

    electives = level.data_level("ECON",major_d_data,course_data,"A&S","Electives")
    electives_sorted = importance.rank_importance(major_d_data,course_data,
    electives,courses_taken,'A&S',"ECON",major_left,major_l_data,
    minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
    result['Electives']['Courses'] = electives_sorted
    result['Electives']['Description'] = None
    result['Electives']['Number'] = data['Electives']['number']

    return result


def parse_CS_CAS(course_data,courses_taken,major_d_data,major_left=None,
major_l_data=None,minor1=None,minor1_data=None,minor2=None,minor2_data=None,minor3=None,minor3_data=None):
    data = major_d_data['A&S']
    result = {}
    section_names = ['Introductory Programming','Core Courses',
    'Math Requirements','CS Electives','Practicum or Project']
    for section in section_names:
        result[section] = {}

    taken_fulfilled = []

    result['Introductory Programming']['Courses'] = data['Introductory Programming']
    result['Introductory Programming']['Description'] = None
    result['Introductory Programming']['Number'] = None
    introductory_taken = course.fulfilled_2dlist(courses_taken,data['Introductory Programming'])
    taken_fulfilled += introductory_taken

    result['Core Courses']['Courses'] = data['Core Courses']
    result['Core Courses']['Description'] = None
    result['Core Courses']['Number'] = None
    core_taken = course.fulfilled_2dlist(courses_taken,data['Core Courses'])
    taken_fulfilled += core_taken

    result['Math Requirements']['Courses'] = data['Math']
    result['Math Requirements']['Description'] = None
    result['Math Requirements']['Number'] = None
    math_taken = course.fulfilled_2dlist(courses_taken,data['Math'])
    taken_fulfilled += math_taken

    # CS Electives
    cs_electives = level.data_level('CS',major_d_data,course_data,
    'A&S','CS Electives')
    simplified_cs_electives = []
    for course_code in cs_electives:
        if not course_code in taken_fulfilled:
            if not course.is_cornell_tech(course_data,course_code):
                simplified_cs_electives.append(course_code)
    cs_electives_sorted = importance.rank_importance(major_d_data,course_data,
    simplified_cs_electives,courses_taken,'A&S',"CS",major_left,major_l_data,
    minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
    result['CS Electives']['Courses'] = cs_electives_sorted
    result['CS Electives']['Description'] = data['CS Electives']['description']
    result['CS Electives']['Number'] = data['CS Electives']['number']

    # Practicum
    practicum = (level.find_CS4XX1(course_data) +
                data["Practicum or Project"]["included"])
    practicum_sorted = importance.rank_importance(major_d_data,course_data,
    practicum,courses_taken,'A&S',"CS",major_left,major_l_data,minor1,minor1_data,minor2,minor2_data,
    minor3,minor3_data)
    result["Practicum or Project"]['Courses'] = practicum_sorted
    result['Practicum or Project']['Description'] = data['Practicum or Project']['description']
    result['Practicum or Project']['Number'] = data['Practicum or Project']['number']

    return result

def parse_INFO_CAS(course_data,courses_taken,major_d_data,major_left=None,
major_l_data=None,minor1=None,minor1_data=None,minor2=None,minor2_data=None,minor3=None,minor3_data=None):
    data = major_d_data['A&S']
    result = {}
    section_names = ["Core Courses","Programming Requirements","Math Requirements",
    "Statistics","Electives","Data Analysis","Data Domain Expertise",
    "Big Data Ethics, Policy and Society","Data Communication"]
    for section in section_names:
        result[section] = {}

    taken_fulfilled = []

    result["Core Courses"]['Courses'] = data["Core Courses"]
    result["Core Courses"]['Description'] = None
    result["Core Courses"]['Number'] = None

    result["Programming Requirements"]['Courses'] = data["Programming Requirements"]
    result["Programming Requirements"]['Description'] = None
    result["Programming Requirements"]['Number'] = None

    result["Math Requirements"]['Courses'] = data["Math Requirements"]
    result["Math Requirements"]['Description'] = None
    result["Math Requirements"]['Number'] = None

    statistics = data["Statistics"]["included"]
    statistics_sorted = importance.rank_importance(major_d_data,course_data,
    statistics,courses_taken,'A&S',"INFO",major_left,major_l_data,minor1,minor1_data,minor2,minor2_data,
    minor3,minor3_data)
    result["Statistics"]['Courses'] = statistics_sorted
    result["Statistics"]['Description'] = data["Statistics"]["description"]
    result["Statistics"]['Number'] = data["Statistics"]["number"]

    electives = level.data_level('INFO',major_d_data,course_data,'A&S','Electives')
    simplified_electives = []
    for course_code in electives:
        if not course.is_cornell_tech(course_data,course_code):
            if not course.is_mps(course_data,course_code):
                simplified_electives.append(course_code)
    electives_sorted = importance.rank_importance(major_d_data,course_data,
    simplified_electives,courses_taken,'A&S',"INFO",major_left,major_l_data,
    minor1,minor1_data,minor2,minor2_data,minor3,minor3_data)
    result["Electives"]['Courses'] = electives_sorted
    result["Electives"]['Description'] = data['Electives']['description']
    result["Electives"]['Number'] = data['Electives']['number']

    data_analysis = data["Data Analysis"]["included"]
    data_analysis_sorted = importance.rank_importance(major_d_data,course_data,
    data_analysis,courses_taken,'A&S',"INFO",major_left,major_l_data,minor1,
    minor1_data,minor2,minor2_data,minor3,minor3_data)
    result["Data Analysis"]['Courses'] = data_analysis_sorted
    result["Data Analysis"]['Description'] = None
    result["Data Analysis"]['Number'] = data["Data Analysis"]["number"]

    data_domain_expertise = data["Data Domain Expertise"]["included"]
    data_domain_expertise_sorted = importance.rank_importance(major_d_data,course_data,
    data_domain_expertise,courses_taken,'A&S',"INFO",major_left,major_l_data,minor1,
    minor1_data,minor2,minor2_data,minor3,minor3_data)
    result["Data Domain Expertise"]['Courses'] = data_domain_expertise_sorted
    result["Data Domain Expertise"]['Description'] = None
    result["Data Domain Expertise"]['Number'] = data["Data Domain Expertise"]["number"]

    ethics = data["Big Data Ethics, Policy and Society"]["included"]
    ethics_sorted = importance.rank_importance(major_d_data,course_data,
    ethics,courses_taken,'A&S',"INFO",major_left,major_l_data,minor1,
    minor1_data,minor2,minor2_data,minor3,minor3_data)
    result["Big Data Ethics, Policy and Society"]['Courses'] = ethics_sorted
    result["Big Data Ethics, Policy and Society"]['Description'] = None
    result["Big Data Ethics, Policy and Society"]['Number'] = data["Big Data Ethics, Policy and Society"]["number"]

    communication = data["Data Communication"]["included"]
    communication_sorted = importance.rank_importance(major_d_data,course_data,
    communication,courses_taken,'A&S',"INFO",major_left,major_l_data,minor1,
    minor1_data,minor2,minor2_data,minor3,minor3_data)
    result["Data Communication"]['Courses'] = communication_sorted
    result["Data Communication"]['Description'] = None
    result["Data Communication"]['Number'] = data["Data Communication"]["number"]

    return result
