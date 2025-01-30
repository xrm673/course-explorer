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

@app.before_request
def load_data():
    load_course_data()
    load_college_data()

# helper for load data
def load_course_data():
    global course_data
    with open('data/course_data/combined/corrected.json', 'r') as file:
        course_data = json.load(file)

# helper for load data
def load_college_data():
    global college_data
    with open('data/college_data/college.json', 'r') as file:
        college_data = json.load(file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'college' not in session:
        return redirect(url_for('select_college'))
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
    minors = college_data["Minors"]
    if request.method == 'POST':
        major1 = request.form.get("major1")
        major2 = request.form.get("major2")
        minor1 = request.form.get("minor1")
        if not major1 or major1 not in majors:
            return "You must select at least one major.", 400
        if major2 and (major2 not in majors or major1 == major2):
            return "Your second major must be different and valid.", 400
        session['major1'] = major1
        session['major2'] = major2 if major2 else None
        session['minor1'] = minor1 if minor1 else None
        return redirect(url_for('select_year'))
    return render_template('select-major.html',majors=majors,minors=minors)

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
    if course.contain_course(course_data,course_code):
        data = course_data[subject][course_code]
    else:
        raise Exception()
    title = data["Title"]
    description = data["Description"]
    credits = data['Credits']
    semesters = data['Semester Offered']
    distributions = data["Distribution"]
    prereq = data["Prerequisites"]
    requirement = data["Specific Requirements"]
    comments = data["Comments"]
    recommend = data["Recommended Prerequisite"]
    permission = data["Permission"]
    return render_template(
        'course.html',
        course_code = course_code,
        title = title,
        description = description,
        credits = credits,
        semesters = semesters,
        distributions = distributions,
        prereq = prereq,
        requirement = requirement,
        comments = comments,
        recommend = recommend,
        permission = permission
        )

@app.route('/<major_displayed>-<college>', methods=['GET'])
def display_major(major_displayed, college):
    courses_taken = session['courses_taken']
    major1 = session["major1"]
    major2 = session["major2"]
    major_d_data = load_major_data(major_displayed)
    minor1 = session["minor1"]
    # minor2 = session["minor2"]
    # minor3 = session["minor3"]
    session['number_int'] = 0
    session['number_list'] = [0]
    if major2:
        if major1 == major_displayed:
            major_left = major2
        if major2 == major_displayed:
            major_left = major1
        major_l_data = load_major_data(major_left)
    else:
        major_left = None
        major_l_data = None
    minor1_data = load_minor_data(minor1) if minor1 else None
    sections = parseMajor.parse_major(course_data,courses_taken,college,
    major_displayed,major_d_data,major_left,major_l_data,minor1,minor1_data)

    simple_sections = {}
    searchable_sections = {}

    for section_name, info in sections.items():
        if isinstance(info['Courses'], list):
            simple_sections[section_name] = info
        else:
            searchable_sections[section_name] = info

    return render_template(
        'display-major.html',
        course_data = course_data,
        courses_taken = session['courses_taken'],
        major=major_displayed,
        college=college,
        simple_sections=simple_sections,
        searchable_sections=searchable_sections,
        number = session['number_int'],
        number_list = session['number_list']
    )

@app.route('/add_course_taken', methods=['POST'])
def add_course_taken():
    data = request.json
    course_code = data.get('course')

    if not course_code:
        return jsonify({'error': 'No course provided'}), 400

    # Initialize session["courses_taken"] if it doesn't exist
    if 'courses_taken' not in session:
        session['courses_taken'] = []
    if not session['courses_taken']:
        session['courses_taken'] = []
    # if course_code not in session['courses_taken']:
    #     session['courses_taken'].append(course_code)
    #     print(session['courses_taken'])
    # return jsonify(session['courses_taken'])

    courses_taken = session['courses_taken'][:]
    if course_code not in courses_taken:
        courses_taken.append(course_code)
        session['courses_taken'] = courses_taken
        print(session['courses_taken'])
    return jsonify(session['courses_taken'])

@app.route('/remove_course_taken', methods=['POST'])
def remove_course_taken():
    data = request.json
    course_code = data.get('course')

    if not course_code:
        return jsonify({'error': 'No course provided'}), 400

    # Check if 'courses_taken' exists in the session
    if 'courses_taken' not in session:
        session['courses_taken'] = []

    courses_taken = session['courses_taken'][:]
    # Remove the course from session['courses_taken'] if it exists
    if course_code in session['courses_taken']:
        courses_taken.remove(course_code)
        session['courses_taken'] = courses_taken

    # Return the updated list of courses
    return jsonify(session['courses_taken'])

@app.route('/check_eligibility', methods=['POST'])
def check_eligibility():
    data = request.json
    course_code = data.get('course')

    if not course_code:
        return jsonify({'error': 'No course provided'}), 400

    courses_taken = session.get('courses_taken', [])
    is_eligible, _ = course.check_eligibility(course_data, courses_taken, course_code)

    return jsonify({'course': course_code, 'is_eligible': is_eligible})

@app.template_filter('extract_subject')
def extract_subject(course_code):
    return course.get_subject(course_code)

@app.template_filter('extract_number')
def extract_number(course_code):
    return course.get_number(course_code)

@app.template_filter('get_recent_semester')
def get_recent_semester(course_code):
    semester_list = course.get_semester_offered(course_data,course_code)
    return semester_list[0]

@app.template_filter('is_eligible')
def is_eligible(course_code):
    courses_taken = session['courses_taken']
    check,list = course.check_eligibility(course_data,courses_taken,course_code)
    return check

def is_group_taken(group, courses_taken):
    return any(course in courses_taken for course in group)

app.jinja_env.globals.update(is_group_taken=is_group_taken)

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

def load_minor_data(minor):
    with open(f"data/minor_data/{minor}.json", 'r') as file:
        minor_data = json.load(file)
    return minor_data


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
