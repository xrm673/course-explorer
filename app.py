"""
Author: Raymond Xu
Start Date: January 3, 2025
"""

from flask import Flask, session, request, jsonify, redirect, url_for, render_template
import json
import re
import special
import parseMajor
import course

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'

course_data = {}
college_data = {}
major1_data = {}
major2_data = {}

CURRENT = 2025
LATEST = 2030

@app.before_first_request
def load_data():
    load_course_data()
    load_college_data()

# helper for load data
def load_course_data():
    global course_data
    with open('data/course_data/combined/combined.json', 'r') as file:
        course_data = json.load(file)

# helper for load data
def load_college_data():
    global college_data
    with open('data/college_data/college.json', 'r') as file:
        college_data = json.load(file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'college' not in session:
        return redirect(url_for('select-college'))
    college = session['college']
    major1_code = session['major1']
    major1 = college_data[college]['Majors'][major1_code]
    major2_code = session['major2']
    if not major2_code == None:
        major2 = college_data[college]['Majors'][major2_code]
    else:
        major2 = None
    return render_template(
        'index.html',
        college_data = college_data,
        college = college,
        major1 = major1,
        major2 = major2,
        major1_code = major1_code,
        major2_code = major2_code,
        year = session['year'])

# @app.route('/get-started', methods=['GET', 'POST'])
# def get_started():
#     if request.method == 'POST':
#         return redirect(url_for('select_college'))
#     return render_template('get-started.html')

@app.route('/select-college', methods=['GET', 'POST'])
def select_college():
    if request.method == 'POST':
        college = request.form.get("college")
        if not college or college not in college_data:
            return "You must select a college.", 400
        session['college'] = college
        return redirect(url_for('select_major'))
    return render_template('select-college.html',colleges=college_data)

@app.route('/select-major', methods=['GET', 'POST'])
def select_major():
    if 'college' not in session:
        return redirect(url_for('select-college'))
    college = session['college']
    majors = college_data[college]['Majors']
    if request.method == 'POST':
        major1 = request.form.get("major1")
        major2 = request.form.get("major2")
        if not major1 or major1 not in majors:
            return "You must select at least one major.", 400
        if major2 and (major2 not in majors or major1 == major2):
            return "Your second major must be different and valid.", 400
        session['major1'] = major1
        session['major2'] = major2 if major2 else None
        return redirect(url_for('select_year'))
    return render_template('select-major.html',majors=majors)

@app.route('/select-year',methods=['GET', 'POST'])
def select_year():
    options = list(range(LATEST, CURRENT-1, -1))
    if request.method == 'POST':
        year = request.form.get("year")
        if not year or int(year) not in options:
            return "You must select a valid year.", 400
        session['year'] = year
        return redirect(url_for('select_courses'))
    return render_template('select-year.html',year_options = options)

@app.route('/select-courses', methods=['GET', 'POST'])
def select_courses():
    if request.method == 'POST':
        courses_taken = request.form.getlist('courses')
        if not courses_taken:
            courses_taken = []
        session['courses_taken'] = courses_taken
        return redirect(url_for('index'))
    return render_template('select-courses.html')

@app.route('/search-courses', methods=['GET'])
def search_courses():
    query = request.args.get('query', '').upper()
    if not query:
        return jsonify([])
    matching_courses = []
    if query.isalpha():
        for subject in course_data:
            if query in subject:
                count = 0
                for course_code, course_info in course_data[subject].items():
                    matching_courses.append({
                        'course_code': course_code,
                        'title': course_info['Title']
                    })
                    count += 1
                    if count == 8:
                        return jsonify(matching_courses)
        return jsonify(matching_courses)
    else:
        query_subject = course.get_subject(query)
        if query_subject in course_data:
            for course_code, course_info in course_data[query_subject].items():
                if query in course_code:
                    matching_courses.append({
                        'course_code': course_code,
                        'title': course_info['Title']
                    })
            return jsonify(matching_courses[:8])
    return jsonify([])

@app.route('/<course_code>',methods = ['GET'])
def display_course(course_code):
    subject = course.get_subject(course_code)
    if subject in course_data and course_code in course_data[subject]:
        data = course_data[subject][course_code]
    else:
        raise Exception()
    title = data["Title"]
    credits = data['Credits']
    semesters = data['Semester Offered']
    distributions = data["Distribution"]
    prereq = data["Prerequisites"]
    return render_template(
        'course.html',
        course_code = course_code,
        title = title,
        credits = credits,
        semesters = semesters,
        distributions = distributions,
        prereq = prereq)

@app.route('/<major>-<college>', methods=['GET'])
def display_major(major, college):
    courses_taken = session['courses_taken']
    # Load data for the major
    major_data = load_major_data(major)
    sections = parseMajor.parse_major(courses_taken,major,college,major_data,course_data)

    # Split sections into simple and searchable based on the structure
    simple_sections = {}
    searchable_sections = {}

    for section_name, info in sections.items():
        # Check if courses are in a nested list (simple sections)
        if isinstance(info['Courses'], list):  # Nested list
            simple_sections[section_name] = info
        else:  # Flat list (searchable sections)
            searchable_sections[section_name] = info

    return render_template(
        'display-major.html',
        course_data = course_data,
        courses_taken = session['courses_taken'],
        major=major,
        college=college,
        simple_sections=simple_sections,
        searchable_sections=searchable_sections
    )

@app.template_filter('extract_subject')
def extract_subject(course_code):
    return course.get_subject(course_code)

@app.template_filter('extract_number')
def extract_number(course_code):
    return course.get_number(course_code)

@app.template_filter('get_recent_semester')
def get_recent_semester(course_code):
    semester_list = course.get_semester_offered(course_code,course_data)
    return semester_list[0]

@app.template_filter('is_eligible')
def is_eligible(course_code):
    courses_taken = session['courses_taken']
    check,list = course.check_eligibility(course_data,courses_taken,course_code)
    return check

# @app.route('/api/search-section-courses', methods=['POST'])
# def search_section_courses():
#     data = request.json
#     print(f"Incoming data: {data}")
#     query = data.get('query', '').upper()
#     remaining_courses = data.get('remaining_courses', [])
#     print(f"Query: {query}, Remaining Courses: {remaining_courses}")
#
#     if not query or not remaining_courses:
#         return jsonify([])
#
#     # Filter remaining courses based on the query
#     matching_courses = [
#         course for course in remaining_courses if query in course.upper()
#     ]
#     print(f"Matching Courses: {matching_courses}")
#
#     # Limit the results to 8 courses
#     return jsonify(matching_courses[:8])

def load_major_data(major):
    with open(f"data/major_data/{major}.json", 'r') as file:
        major_data = json.load(file)
    return major_data


#-----------------------------------------------------------------------------
#helper functions
def load_major1(major1):
    global major1_data
    with open(f"data/major_data/{major1}.json", 'r') as file:
        major1_data = json.load(file)

def load_major2(major2):
    global major2_data
    with open(f"data/major_data/{major2}.json", 'r') as file:
        major2_data = json.load(file)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
