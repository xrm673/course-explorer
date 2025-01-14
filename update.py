"""
Author: Raymond Xu
Start Date: December 23, 2024
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

LATEST_SEMESTER = "SP25"

def write_home_html(semester):
    """
    Write or overwrite an html document of the home page of Cornell class
    roster, with semester defined by client.

    Parameter semester: the semester to search
    Precondition: semester is a str in form of season + year. Season should be 2
    capital letters among "SP","SU","FA","WI"; and year should be a 2-digits int
    Example: "SP25", "FA26"
    """
    assert isinstance(semester,str) and len(semester) == 4
    assert semester[:2] in ["SP","SU","FA","WI"]

    home_url = "https://classes.cornell.edu/browse/roster/" + semester

    response = requests.get(home_url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch the home page. "
            f"Status code: {response.status_code}"
        )

    folder_path = os.path.join("html", semester)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"home_{semester}.html")

    with open(file_path,"w",encoding="utf-8") as writer:
        writer.write(response.text)

def get_subjects(semester):
    """
    Return a dictionary with keys the subject codes and values their
    corresponding name in a given semester

    Parameter semester: the semester to search
    Precondition: semester is a str in form of season + year. Season should be 2
    capital letters among "SP","SU","FA","WI"; and year should be a 2-digits int
    Example: "SP25", "FA26"
    """
    file_path = os.path.join(f"html/{semester}",f"home_{semester}.html")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist."
        f"Ensure `write_home_html` is called first.")
    with open(file_path, "r") as reader:
        home_html = reader.read()

    result = {}

    home_page = BeautifulSoup(home_html,"html.parser")
    li_tags = home_page.find_all("li", {"class": "browse-subjectdescr"})
    for li_tag in li_tags:
        a_tag = li_tag.find("a")  # Get the <a> tag
        subject_link = a_tag["href"]
        pos = subject_link.find("subject/")
        subject_code = subject_link[pos+8:]
        subject_name = a_tag.text
        result[subject_code] = subject_name

    return result

def write_subject_html(semester,subject_code):
    """
    Write or overwrite an html document of a subject page in Cornell's class
    roster of a defined semester

    Parameter semester: the semester to search
    Precondition: semester is a str in form of season + year. Season should be 2
    capital letters among "SP","SU","FA","WI"; and year should be a 2-digits int
    Example: "SP25", "FA26"

    Parameter subject_code: the abbreviation of a subject at Cornell
    Precondition: subject_code is a str
    Example: "AEM", "CS", "PHYS"
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

    folder_path = os.path.join("html",semester)
    os.makedirs(folder_path,exist_ok=True)
    file_path = os.path.join(folder_path, f"{semester}_{subject_code}.html")
    with open(file_path,"w",encoding="utf-8") as writer:
        writer.write(response.text)

    print(f"Successfully write {subject_code}")


def write_all_subjects_html(semester):
    """
    Write or overwrite html documents of all the subject pages of a given
    semester from Cornell's class roster

    Parameter semester: the semester to search
    Precondition: semester is a str in form of season + year. Season should be 2
    capital letters among "SP","SU","FA","WI"; and year should be a 2-digits int
    Example: "SP25", "FA26"
    """
    write_home_html(semester)
    subject_dict = get_subjects(semester)
    count = 0
    for subject_code in subject_dict:
        write_subject_html(semester,subject_code)
        count += 1
    print(count)


write_all_subjects_html(LATEST_SEMESTER)
