"""
Author: Raymond Xu
Date: January 7, 2025
"""
import level
import course

def rank_importance(major_data,course_data,courses,courses_taken,college,major1,major2=None):
    """
    return a sorted dictionary of courses based on the courses taken
    """
    result = {}
    for course in courses:
        score,tags = individual_rank(major_data,course_data,course,courses_taken,college,major1,major2)
        result[course] = (score,tags)
    ranked_courses = dict(sorted(result.items(),key=lambda item: item[1][0],
    reverse=True))
    return ranked_courses

#helper for rank_importance
def individual_rank(major_data,course_data,course_code,courses_taken,college,major1,major2=None):
    """
    return the score and tags of a course based on major(s) and courses taken
    """
    score = 0
    is_eligible,ineligible_courses = course.check_eligibility(course_data,courses_taken,course_code)
    if is_eligible:
        score += 100
    major1_score,tags1 = major_importance(major_data,college,major1,course_code)
    if major2:
        major2_score,tags2 = major_importance(major_data,college,major2,course_code)
    else:
        major2_score = 0
        tags2 = {}
    score = score + major1_score + major2_score
    tags = combine_dictionaries(tags1,tags2)
    return score,tags

# helper for individual_rank
def combine_dictionaries(dict1,dict2):
    """
    combine two dictionaires
    """
    for key in dict2:
        dict1[key] = dict2[key]
    return dict1

def major_importance(major_data,college,major,course_code):
    if major == 'CS' and college == 'A&S':
        return importance_CS_CAS(major_data,course_code)

def importance_CS_CAS(major_data,course_code,core=False,math=False,
cs_electives=False,practicum=False):
    score = 0
    tags = {}
    note = "Not necessarily fulfill the Computer Science major requirement"

    if core == False:
        for core_requirement in major_data["A&S"]['Core']:
            if course_code in core_requirement:
                score += 10
                tags['CS Core'] = "This is a core course of CS major."

    if cs_electives == False:
        min_level = major_data["A&S"]["CS Electives"]["min_level"]
        if level.data_match_level(course_code,major_data,'A&S','CS',"CS Electives"):
            score += 5
            tags[f"{str(min_level)}000+ CS"] = (f"This can be counted as a "
            f"{str(min_level)}000+ CS course")

    return score,tags
