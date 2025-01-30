"""
Author: Raymond Xu
Date: January 7, 2025
"""
import level
import course
import minorImportance

def rank_importance(major_data,course_data,courses,courses_taken,college,
major_displayed,major_left=None,major_l_data=None,minor1=None,minor1_data=None,minor2=None,minor2_data=None,minor3=None,minor3_data=None):
    """
    return a sorted dictionary of courses based on the courses taken
    """
    result = {}
    for course in courses:
        score,tags = individual_rank(major_data,course_data,course,courses_taken,
        college,major_displayed,major_left,major_l_data,minor1,minor1_data,
        minor2,minor2_data,minor3,minor3_data)
        result[course] = (score,tags)
    ranked_courses = dict(sorted(result.items(),key=lambda item: item[1][0],
    reverse=True))
    return ranked_courses

#helper for rank_importance
def individual_rank(major_data,course_data,course_code,courses_taken,college,
major_displayed,major_left=None,major_l_data=None,minor1=None,minor1_data=None,
minor2=None,minor2_data=None,minor3=None,minor3_data=None):
    """
    return the score and tags of a course based on major(s) and courses taken
    """
    score = 0

    course_taken = course.course_taken(course_data,courses_taken,course_code)
    if course_taken:
        score -= 20000

    is_eligible,_ = course.check_eligibility(course_data,courses_taken,
    course_code)
    if is_eligible:
        score += 10000
    college_score,tags_college = college_importance(course_data,college,course_code)
    major_d_score,tags_d = major_importance(course_data,major_data,college,
    major_displayed,course_code)
    if major_left:
        major_l_score,tags_l = major_importance(course_data,major_l_data,college,
        major_left,course_code)
    else:
        major_l_score = 0
        tags_l = {}
    tags = combine_dictionaries(tags_college,tags_l)
    if minor1:
        minor1_score,tags_minor1 = minorImportance.minor_importance(course_data,
        minor1_data,college,minor1,course_code)
    else:
        minor1_score = 0
        tags_minor1 = {}
    score = score + college_score + major_d_score + major_l_score + minor1_score
    tags = combine_dictionaries(tags,tags_minor1)
    # tags = combine_dictionaries(tags_d,tags_l)
    return score,tags

# helper for individual_rank
def combine_dictionaries(dict1,dict2):
    """
    combine two dictionaires
    """
    for key in dict2:
        dict1[key] = dict2[key]
    return dict1

def college_importance(course_data,college,course_code):
    if college == "A&S":
        return importance_CAS(course_data,course_code)

def importance_CAS(course_data,course_code):
    score = 0
    tags = {}
    distr = course.get_distribution(course_data,course_code)
    if distr:
        if "ALC-AS" in distr:
            score += 10
            tags["ALC-AS"] = (f"This can be counted as an Arts, Literature, and "
            f"Culture course in A&S.")
        if "BIO-AS" in distr:
            score += 10
            tags["BIO-AS"] = (f"This can be counted as a Biological Sciences "
            f"course in A&S.")
        if "ETM-AS" in distr:
            score += 10
            tags["ETM-AS"] = (f"This can be counted as a Ethics and Mind "
            f"course in A&S.")
        if "GLC-AS" in distr:
            score += 10
            tags["GLC-AS"] = (f"This can be counted as a Global Citizenship "
            f"course in A&S.")
        if "HST-AS" in distr:
            score += 10
            tags["HST-AS"] = (f"This can be counted as a Historical Analysis "
            f"course in A&S.")
        if "PHS-AS" in distr:
            score += 10
            tags["PHS-AS"] = (f"This can be counted as a Physical Sciences "
            f"course in A&S.")
        if "SCD-AS" in distr:
            score += 10
            tags["SCD-AS"] = (f"This can be counted as a Social Difference "
            f"course in A&S.")
        if "SSC-AS" in distr:
            score += 10
            tags["SSC-AS"] = (f"This can be counted as a Social Sciences "
            f"course in A&S.")
        if "SDS-AS" in distr:
            score += 10
            tags["SDS-AS"] = (f"This can be counted as a Statistics and Data Science "
            f"course in A&S.")
        if "SMR-AS" in distr:
            score += 10
            tags["SMR-AS"] = (f"This can be counted as a Symbolic and "
            f"Mathematical Reasoning course in A&S.")
    return score,tags

def major_importance(course_data,major_data,college,major,course_code):
    if college == 'A&S':
        if major == 'ARTH':
            return importance_ARTH_CAS(course_data,major_data,course_code)
        if major == 'ECON':
            return importance_ECON_CAS(course_data,major_data,course_code)
        if major == 'CS':
            return importance_CS_CAS(course_data,major_data,course_code)
        if major == 'INFO':
            return importance_INFO_CAS(course_data,major_data,course_code)

def importance_ARTH_CAS(course_data,major_data,course_code):
    score = 0
    tags = {}
    for core_group in major_data["A&S"]["Core Courses"]:
        if course_code in core_group:
            score += 10
            tags['ARTH Core'] = "This is a core course of Art History major"

    if course_code in level.data_only_level(course_data,major_data,"A&S","ARTH",
    '2000 Level'):
        score += 5
        tags['ARTH 2000'] = "This is a 2000 level Art History course."

    if course_code in level.data_only_level(course_data,major_data,"A&S","ARTH",
    '3000 Level'):
        score += 5
        tags['ARTH 3000'] = "This is a 3000 level Art History course."

    if course_code in level.data_only_level(course_data,major_data,"A&S","ARTH",
    '4000 Level'):
        score += 5
        tags['ARTH 4000'] = "This is a 4000 level Art History course."

    if course_code in level.data_level("ARTH",major_data,course_data,"A&S",
    '3000+'):
        score += 5
        tags['ARTH 3000+'] = "This is a 3000+ Art History course."

    return score,tags

def importance_ECON_CAS(course_data,major_data,course_code):
    score = 0
    tags = {}

    for basic_group in major_data["A&S"]["Basics"]:
        if course_code in basic_group:
            score += 10
            tags["ECON Basics"] = "This is a basic course required by Economics major."

    for core_group in major_data["A&S"]["Core Courses"]:
        if course_code in core_group:
            score += 10
            tags["ECON Core"] = "This is a core course required by Economics major."

    electives = level.data_level("ECON",major_data,course_data,"A&S","Electives")
    if course_code in electives:
        score += 5
        tags["ECON Electives"] = "This can be counted as an elective for CS major."

    return score,tags

def importance_CS_CAS(course_data,major_data,course_code,introductory=False,
core=False,math=False,cs_electives=False,practicum=False):
    score = 0
    tags = {}

    if introductory == False:
        for introductory_requirement in major_data["A&S"]['Introductory Programming']:
            if course_code in introductory_requirement:
                score += 10
                tags['Introductory CS'] = "This is a introductory programming course."

    if core == False:
        for core_requirement in major_data["A&S"]['Core Courses']:
            if course_code in core_requirement:
                score += 10
                tags['CS Core'] = "This is a core course of CS major."

    if cs_electives == False:
        min_level = major_data["A&S"]["CS Electives"]["min_level"]
        if level.data_match_level(course_data,major_data,course_code,'A&S','CS',"CS Electives"):
            score += 5
            tags[f"{str(min_level)}000+ CS"] = (f"This can be counted as a "
            f"{str(min_level)}000+ CS course")

    return score,tags

def importance_INFO_CAS(course_data,major_data,course_code):
    score = 0
    tags = {}
    for core_group in major_data["A&S"]["Core Courses"]:
        if course_code in core_group:
            score += 10
            tags['INFO Core'] = "This is a core course of INFO major"

    for cs_group in major_data["A&S"]["Programming Requirements"]:
        if course_code in cs_group:
            score += 5
            tags['INFO Programming'] = "This is can fulfill a programming requirement of INFO major"

    for math_group in major_data["A&S"]["Math Requirements"]:
        if course_code in math_group:
            score += 5
            tags['INFO Math'] = "This is can fulfill a math requirement of INFO major"

    if course_code in major_data["A&S"]["Statistics"]["included"]:
        score += 5
        tags['INFO Stats'] = "This is can fulfill a statistics requirement of INFO major"

    if course_code in level.data_level('INFO',major_data,course_data,'A&S','Electives'):
        score += 5
        tags['INFO Electives'] = "This is can be an elective of INFO major"

    return score,tags
