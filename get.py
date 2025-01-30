"""
Author: Raymond Xu
Start Date: December 23, 2024
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import os

LATEST_SEMESTER = "SP25"


def get_subjects(semester):
    """
    Fetch the HTML document of the Cornell class roster home page for the given
    semester. Parse the home page HTML and return a dictionary with subject
    codes and their names.

    Parameter semester: the semester to search
    Precondition: semester is a str in form of season + year. Season should be 2
    capital letters among "SP","SU","FA","WI"; and year should be a 2-digits int
    Example: "SP25", "FA26"
    """
    assert isinstance(semester, str) and len(semester) == 4
    assert semester[:2] in ["SP", "SU", "FA", "WI"]

    home_url = f"https://classes.cornell.edu/browse/roster/{semester}"
    response = requests.get(home_url)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch the home page. "
            f"Status code: {response.status_code}"
        )

    result = {}

    home_page = BeautifulSoup(response.text,"html.parser")
    li_tags = home_page.find_all("li", {"class": "browse-subjectdescr"})
    for li_tag in li_tags:
        a_tag = li_tag.find("a")  # Get the <a> tag
        subject_link = a_tag["href"]
        pos = subject_link.find("subject/")
        subject_code = subject_link[pos+8:]
        subject_name = a_tag.text
        result[subject_code] = subject_name

    return result

def get_courses(semester,subject_code,max_level=5):
    """
    Return a list of courses of a given subject in a semester with a specified
    max level of course. For example, if max_level is set to 5, this will return
    all the courses of this subject whose course code starts from 1 to 5.

    Parameter semester: the semester to search
    Precondition: semester is a str in form of season + year. Season should be 2
    capital letters among "SP","SU","FA","WI"; and year should be a 2-digits int
    Example: "SP25", "FA26"

    Parameter subject_code: the abbreviation of a subject at Cornell
    Precondition: subject_code is a str
    Example: "AEM", "CS", "PHYS"

    Parameter max_level: the max level of course returned
    Precondition: max_level is an int in [1,9]
    """
    subject_url = (
        f"https://classes.cornell.edu/browse/roster/{semester}/"
        f"subject/{subject_code}"
    )
    response = requests.get(subject_url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch the {subject_code} page. "
            f"Status code: {response.status_code}"
        )
    subject_page = BeautifulSoup(response.text,"html.parser")
    subject_codes = subject_page.find_all("div",class_="title-subjectcode")
    result = []
    for code in subject_codes:
        pos = code.text.find(" ")
        if int(code.text[pos+1]) > max_level:
            break
        subject_code = code.text[:pos] + code.text[pos+1:]
        result.append(subject_code)
    return result

def get_all_courses(semester,max_level=5):
    """
    Return a list that contains all the courses provided by Cornell in a given
    semester

    Parameter semester: the semester to search
    Precondition: semester is a str in form of season + year. Season should be 2
    capital letters among "SP","SU","FA","WI"; and year should be a 2-digits int
    Example: "SP25", "FA26"
    """
    subject_dict = get_subjects(semester)
    result = []
    for subject in subject_dict:
        result.append(get_courses(semester,subject,max_level))
    return result

def get_course_details(semester,course_code):
    """
    Return a list that contains the code, title, credits, distribution
    categories, prerequisite, corequisite, prerequisite and corequisite,
    original prerequisite text, whether they need a note of a given course. If
    the course is not found in the given semester, throw an Exception

    Parameter semester: the semester to search
    Precondition: semester is a str in form of season + year. Season should be 2
    capital letters among "SP","SU","FA","WI"; and year should be a 2-digits int
    Example: "SP25", "FA26"

    Parameter course_code: the code of a given course
    Precondition: course_code is a str in format "subject_code+number", such as
    "CS1110"
    """
    match = re.match(r"([A-Za-z]+)(\d+)", course_code)
    if match:
        subject = match.group(1)
        code = match.group(2)

    course_url = (f"https://classes.cornell.edu/browse/roster/{semester}"
                  f"/class/{subject}/{code}")
    response = requests.get(course_url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch the {course_code} page. "
            f"Status code: {response.status_code}"
        )
    course_page = BeautifulSoup(response.text,"html.parser")

    course_title = course_page.find("div", class_="title-coursedescr")
    description = course_page.find("p", class_="catalog-descr")
    heading = course_page.find("p", class_="heading")
    prereq = course_page.find("span", class_="catalog-prereq")
    comments = course_page.find("span",class_="catalog-comments")
    credits = course_page.find("span", class_="credits")
    distr = course_page.find("span", class_="catalog-distr")
    permission = course_page.find("span",class_="catalog-permiss")
    foot_note = course_page.find("li",class_="section-alt section-alt-details notes")

    description_text = description.text if description else None
    permission_text = permission.text if permission else None
    prereq_text = prereq.text if prereq else None
    comments_text = comments.text if comments else None

    if description_text:
        description_text.replace('\xa0', ' ').replace("—","--").strip()

    if permission_text:
        permission_text.replace("\xa0", " ").replace("—","--")

    combined_courses = None
    if heading:
        combined_with_list = heading.find_all("a")
        if combined_with_list:
            combined_courses = []
            for combined_with in combined_with_list:
                combined_course = combined_with.text
                pos = combined_course.find(" ")
                if pos != -1:
                    combined_course = combined_course[:pos] + combined_course[pos+1:]
                    combined_courses.append(combined_course)

    foot_note_text = None
    if foot_note:
        foot_note = foot_note.find("p")
        if foot_note:
            foot_note_text = foot_note.text

    recommended_prereq = None
    if comments_text:
        comments_text.replace("\xa0", " ").replace("—","--")
        pos_comments = comments_text.find("Comments ")
        comments_text = comments_text[9:]

        if re.search(r"Recommended prerequisite:", comments_text, re.IGNORECASE):
            recommended_prereq = comments_text
            comments_text = None

        elif comments_text.find("Prerequisite:") != -1:
            prereq_text = comments_text
            comments_text = None

    if prereq_text:
        prereq_text = prereq_text.replace("\xa0", " ").replace("—","--")
        pos_preco = prereq_text.find("Prerequisites/Corequisites ")
        pos_pre = prereq_text.find("Prerequisites/Corequisites ")
        if pos_preco == 0:
            prereq_text_simplified = prereq_text[27:]
        else:
            prereq_text_simplified = prereq_text
    else:
        prereq_text_simplified = None

    details = {
        "Title" : course_title.text,
        "Course Code" : course_code,
        "Description" : description_text,
        "Combined Course" : combined_courses,
        "Semester Offered" : [semester],
        "Credits" : credits_to_list(credits.text),
        "Distribution" : extract_distr(distr.text) if distr else None,
        "Prerequisites" : [], "Corequisites" : [],
        "Prerequisites or Corequisites" : [],
        "Specific Requirements" : prereq_text_simplified,
        "Comments" : comments_text if comments_text else None,
        "Recommended Prerequisite" : recommended_prereq if recommended_prereq else None,
        "Permission" : permission_text,
        "Foot Note" : foot_note_text,
        "Need Note" : False
    }

    if prereq_text:
        prereq_list = separate_prereq(prereq_text)

        prerequisite = parse_prerequisites(prereq_list[0])
        details["Prerequisites"] = prerequisite[:-1]

        coreq = parse_prerequisites(prereq_list[1])
        details["Corequisites"] = coreq[:-1]

        precoreq = parse_prerequisites(prereq_list[2])
        details["Prerequisites or Corequisites"] = precoreq[:-1]

        last_pre = prerequisite[-1] if prerequisite else None
        last_co = coreq[-1] if coreq else None
        last_preco = precoreq[-1] if precoreq else None
        need_note = last_pre or last_co or last_preco
        if need_note == None:
            need_note = False
        details["Need Note"] = need_note

    print(f"Successfully get {course_code}")
    return details

def parse_prerequisites(prereq_text):
    """
    Parse prerequisite text into a nested list, with the last element of the
    nested list indicating whether it needs further explanation.
    "A or B and C" should be converted to [[A,B],C]

    If the prereq text is in format "topic (e.g. course1, course2)", or
    "1) topic: ...; 2) topic ..." only keep the topic part and replace the topic
    into several specified courses. For example, "linear algebra" is replaced by
    "MATH 2210 or MATH 2310 or MATH 2940".

    For text in "a, b, c, or d" structures, replace each comma with "or";
    for text in "a, b, c or d" structures, replace each comma with "and";
    for "a/b", replace "/" with "or"; replace each ";" with "and".

    Split each text by "and", and then split each sub-text by "or". Only keep
    the course code part in the text and append them into a nested list. Remove
    any repeated course in the nested list.

    Parameter prereq_text: The raw prerequisite text.
    Precondition: a str from Cornell's class roster
    """
    if not prereq_text:
        return []

    prereq_text = prereq_text.replace("\xa0", " ")
    note = False

    patterns = [
        (r"\(.*?\)", ""), (r"For\s.*?majors[:;].*?[.;]", ""),
        (r"Note:.*?;", ""), (r"[A-Za-z\s]+(?:degree|experience),", ""),
        (r"([A-Z]+\s\d{4})-([A-Z]+\s\d{4})",r"\2")
    ]
    for pattern,replace in patterns:
        if re.search(pattern, prereq_text, flags=re.IGNORECASE):
            prereq_text=re.sub(pattern,replace,prereq_text,flags=re.IGNORECASE)
            note = True

    if re.search(r"\d\)\s*.*?:", prereq_text):
        # print("1)")
        # check structure "1)...; 2)...; 3)...;
        matches = re.findall(r"\d\)\s*(.*?):", prereq_text)
        topics = [match.strip() for match in matches]
        prereq_text = " and ".join(topics)
        note = True
    if prereq_text.find(", or permission of the instructor.")!= -1:
        # print("instructor")
        prereq_text=prereq_text.replace(", or permission of the instructor.","")
        note = True
    if prereq_text.find(", or permission of instructor.")!= -1:
        # print("instructor")
        prereq_text=prereq_text.replace(", or permission of instructor.","")
        note = True
    if prereq_text.find("performance")!=-1 or prereq_text.find("excellent")!=-1:
        # print("performance")
        note = True

    if re.search(r',\s*or\s', prereq_text):
        # check structure A, B, or C
        prereq_text = re.sub(r',(?=\s*[^o])', ' or ', prereq_text)
        # replace "," with " or "

    prereq_text = re.sub(r"[;,]\s*$", "", prereq_text) # remove trailing semicolons

    prereq_text = prereq_text.replace(", ", " and ")
    prereq_text = prereq_text.replace(";", " and ")
    prereq_text = prereq_text.replace("/", " or ")

    replacements = {
    "linear algebra":"MATH 2210 or MATH 2230 or MATH 2310 or MATH 2940",
    "single-variable calculus": "MATH 1910 or MATH 1120",
    "calculus": "MATH 1120 or MATH 1910 or MATH 1920 or MATH 2220 or MATH 2240",
    "multi-variable calculus": "MATH 1920 or MATH 2220 or MATH 2240",
    "core statistics": "STSCI 2100 or MATH 1710",
    "probability theory":("BTRY 3080 or CS 2800 or ECON 3130 or ENGRD 2700 or "
    "MATH 4710"),

    "one programming course": "CS 1110 or CS 1112 or CS 1132 or CS 1133",
    "knowledge of programming": "CS 1110 or CS 1112 or CS 1132 or CS 1133",
    "core programming": "CS 1110 or CS 1112",
    "Python":"CS 1110 or CS 1112 or CS 1133",
    "MATLAB": "CS 1132", "C++":"CS 2024",
    "programming proficiency": "CS 2110 or CS 2112",
    "proficient with programming": "CS 2110 or CS 2112",
    "data structures": "CS 2110 or CS 2112",
    "discrete math": "CS 2800",
    "discrete mathematics": "CS 2800",
    "introductory ML course": "CS 3780",
    "numerical methods": "CS 4210 or CS 4220",
    }

    for topic,course in replacements.items():
        if re.search(rf"\b{re.escape(topic)}\b",
        prereq_text, flags=re.IGNORECASE):
            prereq_text = re.sub(
            rf"\b{re.escape(topic)}\b",
            course,prereq_text,flags=re.IGNORECASE)
            note = True

    and_split = re.split(r"\s+and\s+", prereq_text)
    or_split = [re.split(r"\s+or\s+", item) for item in and_split]

    # Matches patterns like "CS 1110", "MATH 1920"
    course_code_pattern = r"[A-Z]{2,10}\s\d{4}"
    nested_list = []
    for group in or_split:
        course_list = [
            re.sub(r"\s", "", match.group()) # Remove spaces in matched course codes
            for item in group
            for match in re.finditer(course_code_pattern, item)
        ]
        nested_list.append(course_list)
    for sublist in nested_list:
        if len(sublist) == 0:
            # print("empty")
            note = True
    cleaned_list = [sublist for sublist in nested_list if sublist]
    result = remove_repeat(cleaned_list)
    result.append(note)
    return result

def separate_prereq(text):
    """
    Return a list that separates prereq and coreq

    Use re search to find "Prerequisite:", "Corequisite:", and
    "Prerequisite or corequisite:", append words follow them in a list.

    Parameter text: text is the string that would be separated
    Precondition: text is a str object
    """
    text = text.replace("Prerequisite: ","A_Prerequisite: ")
    text = text.replace("Prerequisite or corequisite: ",
    "B_Prerequisite or corequisite: ")
    text = text.replace("Corequisite: ","C_Corequisite: ")

    prereq_match = re.search(
        r"a_prerequisite:(.*?)(b_prerequisite or corequisite|c_corequisite|$)",
        text,
        re.IGNORECASE
    )

    prereq_or_coreq_match = re.search(
        r"b_prerequisite or corequisite:(.*?)(c_corequisite|$)",
        text,
        re.IGNORECASE
    )

    coreq_match = re.search(r"c_corequisite:(.*)", text, re.IGNORECASE)

    for_roles_match = re.search(
        r"Prerequisite for\s.*?:.*?[.;]",
        text,
        re.IGNORECASE
    )

    result = []

    prereq = prereq_match.group(1).strip() if prereq_match else None
    result.append(prereq)

    coreq = coreq_match.group(1).strip() if coreq_match else None
    result.append(coreq)

    if prereq_or_coreq_match:
        prereq_or_coreq = prereq_or_coreq_match.group(1).strip()
    else:
        prereq_or_coreq = None
    result.append(prereq_or_coreq)

    return result

def remove_repeat(nested_list):
    """
    Return a nested list with repeated element removed

    It first checks and removes repeated sublists, and then it checks and
    removes repeated individual element in the nested list.

    Parameters nested_list: A nested list of courses.
    Precondition: nested_list is a 2D list
    """
    unique_sublists = list(set(map(tuple, nested_list)))

    nested_list = [list(sublist) for sublist in unique_sublists]

    course_to_sublist = {}

    nested_list_sorted = sorted(nested_list, key=len)

    for sublist in nested_list_sorted:
        for course in sublist:
            if course not in course_to_sublist:
                course_to_sublist[course] = sublist

    result = []
    for sublist in nested_list:
        unique_courses = [course for course in sublist
        if course_to_sublist[course] == sublist]
        result.append(unique_courses)

    return result

def extract_distr(text):
    """
    Return a list that contains each distribution category as individual element

    Precondition: text is a str
    """
    matches = re.findall(r"\(([^)]+)\)", text)
    result = []
    for categories in matches:
        result.extend([category.strip() for category in categories.split(",")])
    return result

def credits_to_list(credit_str):
    """
    Return a list that contains credit options of the course

    Precondition: credit_str is a str in format number + "Credits"
    (eg. "4 Credits") or range + Credits (eg. "1-2 Credits")
    """
    credit_str = credit_str.replace("Credits", "").strip()
    credit_str = credit_str.replace("Credit", "").strip()

    if "-" in credit_str:
        credit_range = credit_str.split("-")
        low = float(credit_range[0])
        high = float(credit_range[1])
        credit_list = [low]
        while low < high:
            low += 1
            credit_list.append(low)
    else:
        credit_list = [float(credit_str)]

    return credit_list

def get_subject_details(semester,subject_code,max_level=5):
    """
    Return a list of all course details of a given subject in a given semester
    with a specified max_level of courses.

    Parameter semester: the semester to search
    Precondition: semester is a str in form of season + year. Season should be 2
    capital letters among "SP","SU","FA","WI"; and year should be a 2-digits int
    Example: "SP25", "FA26"

    Parameter subject_code: the abbreviation of a subject at Cornell
    Precondition: subject_code is a str
    Example: "AEM", "CS", "PHYS"

    Parameter max_level: the max level of course returned
    Precondition: max_level is an int in [1,9]
    """
    courses = get_courses(semester,subject_code,max_level)
    result = {}
    for course in courses:
        course_details = get_course_details(semester,course)
        result[course] = course_details
    return result

def get_three_years(latest_semester,subject_code,max_level=5):
    """
    """
    course_dict = get_subject_details(latest_semester,subject_code,max_level)
    season = latest_semester[:2]
    year = int(latest_semester[2:])
    count = 0
    while count < 6:
        if season == "SP":
            season = "FA"
            year -= 1
        elif season == "FA":
            season = "SP"
        semester = season + str(year)
        courses = get_courses(semester,subject_code,max_level)
        for course in courses:
            if course in course_dict:
                course_dict[course]["Semester Offered"].append(semester)
            else:
                course_dict[course] = get_course_details(semester,course)
        count += 1
    return course_dict


def save_one_semester(semester,subject_code,max_level=5):
    """
    convert the dictionary to a json file
    """
    data = get_subject_details(semester,subject_code,max_level)
    file_name = f"{semester}_{subject_code}.json"
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def save_all(subject_code,semester=LATEST_SEMESTER,max_level=5):
    """
    convert the dictionary to a json file
    """
    data = get_three_years(semester,subject_code,max_level)
    os.makedirs('data/course_data', exist_ok=True)
    file_path = os.path.join('data', 'course_data', f"{subject_code}.json")
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def combine_all():
    data_dir = 'data/course_data'
    combined = {}
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                combined[filename.split(".")[0]] = data
    output_dir = os.path.join(data_dir, 'combined')
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'combined.json')
    with open(filepath , 'w') as json_file:
        json.dump(combined,json_file,indent=4)

if __name__ == "__main__":
    save_all('ECON')
    combine_all()
# "CS4744" "CS5775" "MATH4030" "INFO3140" "INFO3152" "INFO4152" "INFO5152"
# 'CS4210' (FA24), 'CS4745' (FA24)
