想实现的功能：
1. 用户选择major或minor，显示required的课
智能排课，"You need at least n semesters to complete this major"

2. 给课评级，优先显示最重要的课
对于每一个major / minor requirement和学院requirement，根据prerequisite顺序，课程offer的学期，major requirement，学院requirement，minor requirement，课程评分，优先显示能上的课 / 智能推荐每个学期可以上的课；保证课程的时间不重复，选择了一门课以后就黑掉其他重复的课

一上来先列举重叠最多的requirement（智能推荐），然后再细分到college，major，minor


3. 输入上过的课，显示可以再上的课

4. 用户给每门课的难度评分，包括workload、考试数量、得分情况等

5. 按话题/兴趣来搜索

6. 简单搜索各major / minor的要求

7. show different pathways


和CoursePlan的区别：combine college, major, minor requirements, pre-requisite order, time, and course rates，为每门课计算出一个分数并排序
和Pathway的区别：更新数据！需要一个算法可以很简单地更新数据库

equivalent看forbidden overlap

CS1110: N/A
CS1112: Prerequisites/Corequisites Prerequisite: MATH 1110 or equivalent.
CS1132: N/A
CS1133: N/A
CS1340: N/A
CS1700: N/A
CS1998: N/A
CS2043: Prerequisites/Corequisites Prerequisite: one programming course or equivalent programming experience.
CS2110: Prerequisites/Corequisites Prerequisite: CS 1110 or CS 1112 or equivalent course on programming in a procedural language.
CS2800: Prerequisites/Corequisites Prerequisite or corequisite: MATH 1110 or equivilent, one programming course or permission of instructor.
CS3110: Prerequisites/Corequisites Prerequisite: CS 2110 or equivalent programming experience. Prerequisite or corequisite: CS 2800.
CS3152: Prerequisites/Corequisites Prerequisite: CS 2110 for programmers, or permission of the instructor. Corequisite: ENGRC 3152.
CS3410: Prerequisites/Corequisites Prerequisite: CS 2110 or equivalent programming experience.
CS3420: Prerequisites/Corequisites Prerequisite: ECE 2300/ENGRD 2300.
CS3700: Prerequisites/Corequisites Prerequisite: CS 2110/ENGRD 2110 and CS 2800, or by permission of instructor.
CS3780: Prerequisites/Corequisites Prerequisite: probability theory (e.g. BTRY 3080, CS 2800, ECON 3130, ENGRD 2700, MATH 4710) and linear algebra (e.g. MATH 2210, MATH 2310, MATH 2940), single-variable calculus (e.g. MATH 1110, MATH 1920) and programming proficiency (e.g. CS 2110).
CS4090: N/A
CS4152: Prerequisites/Corequisites Prerequisite: CS 3152, CS 3300 or CS 3700 or CS 4620 or CS 5414. Corequisite: ENGRC 4152.
CS4220: Prerequisites/Corequisites Prerequisite: MATH 2210 or MATH 2940 or equivalent.
CS4300: Prerequisites/Corequisites Prerequisite: 1) linear algebra: strong performance in MATH 2940 or equivalent; 2) discrete math: strong performance in CS 2800 or equivalent. Note: the linear algebra and discrete math requirements can also be fulfilled with a strong performance in INFO 2950; and 3) programming proficiency: CS 2110 or equivalent with strong Python skills and familiarity with IPython Notebooks, or permission of instructor.
CS4410: Prerequisites/Corequisites Prerequisite: CS 3410 or CS 3420.
CS4411: Prerequisites/Corequisites Corequisite: CS 4410.
CS4450: N/A
CS4670: Prerequisites/Corequisites Prerequisite: CS 2110, CS 2800, MATH 1920 or equivalent and MATH 2310 or MATH 2940 or equivalent.
CS4701: Prerequisites/Corequisites Prerequisite: at least one of the following courses: CS 3700, CS 3780, CS 4670, CS 4740, ECE 4200, ORIE 3741, STSCI 3740, or their equivalents. 
CS4740: N/A
CS4744: Prerequisites/Corequisites Prerequisite: Elementary Python (ex. CS 1133), LING 1101 or CS 2800 or PHIL 2310; for CS majors: Elementary Python and CS 2800.
CS4754: Prerequisites/Corequisites Prerequisite or corequisite: INFO 4320, or an equivalent mechatronics course, or permission of instructor.
CS4756: Prerequisites/Corequisites Prerequisite: CS 2800, probability theory (e.g. BTRY 3080, ECON 3130, MATH 4710, ENGRD 2700), linear algebra (e.g. MATH 2940), calculus (e.g. MATH 1920) , programming proficiency (e.g. CS 2110), and CS 3780 or equivalent or permission of instructor.
CS4758: Prerequisites/Corequisites Prerequisite: MATLAB programming.
CS4782: Prerequisites/Corequisites Prerequisite: CS 2110 or equivalent and CS 3780 or ECE 4200 or STSCI 3740 and CS 1110 or CS 1112.
CS4789: Prerequisites/Corequisites Prerequisite: CS 3780 or equivalent.
CS4810: Prerequisites/Corequisites Prerequisite: CS 2800 or permission of instructor.
CS4813: N/A
CS4820: Prerequisites/Corequisites Prerequisite: CS 2800, CS 3110. 
CS4850: Prerequisites/Corequisites Prerequisite: CS 2800, MATH 1910, MATH 1920, MATH 2210 or MATH 2940.
CS4852: Prerequisites/Corequisites Prerequisite: INFO 2040, CS 2800 or equivalent.
CS4997: N/A
CS4998: N/A
CS4999: N/A
CS5150: Prerequisites/Corequisites Prerequisite: CS 2110 or equivalent experience programming in Java or C++.
CS5152: Prerequisites/Corequisites Prerequisite: CS 3152, CS 3300 or CS 4620 or CS 3700 or CS 5414. Corequisite: ENGRC 5152.
CS5223: Prerequisites/Corequisites Prerequisite: MATH 2210 or MATH 2940 or equivalent, knowledge of programming, CS 3220 or CS 4210/MATH 4250 or permission of instructor.
CS5304: N/A
CS5342: N/A
CS5356: Prerequisites/Corequisites Prerequisite: CS 2110 or CS 2112.
CS5410: Prerequisites/Corequisites Prerequisite: CS 3410 or CS 3420.
CS5411: Prerequisites/Corequisites Corequisite: CS 5410.
CS5430: Prerequisites/Corequisites Prerequisite: CS 4410.
CS5433: Prerequisites/Corequisites Prerequisite: a good level of programming experience—specifically, the ability to deal with challenging programming tasks—familiarity with common algorithms and data structures, and an understanding of basic concepts in discrete mathematics.
CS5435: Prerequisites/Corequisites Prerequisite: CS 2800 or CS 4820 or permission of instructor.
CS5456: N/A
CS5643: Prerequisites/Corequisites Prerequisite: CS 4620 or equivalent; MATH 1120,  MATH 1920, or equivalent; MATH 2210, MATH 2940, or equivalent; PHYS 1112 or equivalent.
CS5670: Prerequisites/Corequisites Prerequisite: CS 2110, CS 2800, MATH 1920 or equivalent and MATH 2310 or MATH 2940 or equivalent (Ithaca only).
CS5700: N/A
CS5726: Prerequisites/Corequisites Prerequisite: ORIE 5750 or CS 5785.
CS5740: N/A
CS5756: Prerequisites/Corequisites Prerequisite: CS 2800, probability theory (e.g. BTRY 3010, ECON 3130, MATH 4710, ENGRD 2700), linear algebra (e.g. MATH 2940), calculus (e.g. MATH 1920), programming proficiency (e.g. CS 2110), and CS 3780 or equivalent or permission of instructor.
CS5758: N/A
CS5775: Prerequisites/Corequisites Prerequisite: undergraduate ECE/CS degree, programming experience, introductory ML course.
CS5780: Prerequisites/Corequisites Prerequisite: CS 2800, probability theory (e.g. BTRY 3080, ECON 3130, MATH 4710, ENGRD 2700), linear algebra (e.g. MATH 2940), calculus (e.g. MATH 1920), and programming proficiency (e.g. CS 2110).
CS5782: Prerequisites/Corequisites Prerequisite: ECE 4200, STSCI 3740, CS 1110, CS 3780, and CS 2110.
CS5789: Prerequisites/Corequisites Prerequisite: CS 5780 or equivalent.
CS5820: N/A
CS5850: Prerequisites/Corequisites Prerequisite: CS 2800, MATH 1910, MATH 1920, MATH 2210 or MATH 2940.
CS5996: N/A
CS5998: N/A
CS5999: N/A
CS6110: N/A
CS6120: Prerequisites/Corequisites Prerequisite: CS 4120 or CS 5120.
CS6156: Prerequisites/Corequisites Prerequisite: graduate standing in CS or CS majors with CS 3110 grade of B+ or better.
CS6230: N/A
CS6241: Prerequisites/Corequisites Prerequisite: strong background in linear algebra, prior exposure to numerical methods.
CS6386: N/A
CS6412: N/A
CS6458: N/A
CS6682: Prerequisites/Corequisites Prerequisite: Python, MATH 2210, CS 2110, or CS 2112.
CS6751: Prerequisites/Corequisites Prerequisite: Proficiency in C++ or Python, and familiarity with ROS.
CS6754: Prerequisites/Corequisites Prerequisite: Python programming experience.
CS6785: Prerequisites/Corequisites Prerequisite: CS 2110, MATH 1920, MATH 2940, MATH 4710, or permission of instructor.
CS6802: Prerequisites/Corequisites Prerequisite: MATH 4310 or permission of instructor.
CS6817: Prerequisites/Corequisites Prerequisite: CS 4820.
CS7090: N/A
CS7190: Prerequisites/Corequisites Prerequisite: CS 6110 or permission of instructor.
CS7290: N/A
CS7390: N/A
CS7490: N/A
CS7690: N/A
CS7790: N/A
CS7794: N/A
CS7796: N/A
CS7890: N/A
CS7999: N/A

from flask import Flask, session, request, jsonify

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'

class User:
    def __init__(self, username, major=None, courses_taken=None):
        self.username = username
        self.major = major if major else []
        self.courses_taken = courses_taken if courses_taken else []

    def set_major(self, major):
        self.major = major

    def add_course(self, course):
        if course not in self.courses_taken:
            self.courses_taken.append(course)

    def remove_course(self, course):
        if course in self.courses_taken:
            self.courses_taken.remove(course)

    def get_user_data(self):
        return {
            "username": self.username,
            "major": self.major,
            "courses_taken": self.courses_taken
        }

@app.route('/set_major', methods=['POST'])
def set_major():
    username = request.json.get("username")
    major = request.json.get("major")
    
    if username not in session:
        session[username] = User(username)
    
    user = session[username]
    user.set_major(major)
    
    return jsonify(user.get_user_data())

@app.route('/add_course', methods=['POST'])
def add_course():
    username = request.json.get("username")
    course = request.json.get("course")
    
    if username not in session:
        session[username] = User(username)
    
    user = session[username]
    user.add_course(course)
    
    return jsonify(user.get_user_data())

@app.route('/get_user', methods=['GET'])
def get_user():
    username = request.args.get("username")
    
    if username in session:
        user = session[username]
        return jsonify(user.get_user_data())
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)


I want my website can recommend users the course they can take in each future semesters, according to their major requirement, graduation year, and the course they have taken. After the user has chosen his major and year, I'll show him his major requirement, with a bunch of courses listed under each requirement. Then, he can select the course he has taken. Each time he selects a course, the system will be updated to recommend the most necessary course he needs to take. This is my current code: