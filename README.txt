The Course Explorer Website is developed by Raymond Xu since December 2024.

This program intends to help users exploring and selecting courses and majors at Cornell University. It displays major requirements and dynamically suggests courses for each requirement based on the user’s preference.

This program uses web scraping to obtain data from Cornell's Class Roster (get.py), Python language and Flask framework to develop its backend (app.py), and JavaScript, HTML, and CSS to develop the frontend (check templates and static folder). The program includes helper functions written in multiple files, such as course.py, importance.py, level.py 

1. Show major requirement

2. Show prerequisites

3. Ranking
According to :
	1. eligibility
	2. overlapped course for college requirement (distribution)
	3. overlapped course for other major / minors / tracks requirements
	4. by difficulty (CUReview) (workload, number of prelims)
	5. by instructor (CUReview & Rate My Professor)

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