# Course Explorer
Developed by Raymond Xu since December 2024. The project is still in progress.

## Overview
The Course Explorer helps users explore and select courses and majors at Cornell University. It displays major requirements and dynamically suggests courses for each requirement based on the user’s preferences.

To use the program, users first select their college, major(s), minor(s), graduation year, and the courses they have taken. After then, the main page will display the selected majors and minors. By clicking on a major / minor, users can see its specific requirements. Major requirements are categorized into sections such as "Core Courses", "Electives", "Math Requirements", etc.

For requirement sections with more than four course options, courses are ranked based on user preferences. Prioritization follows these criteria: 
1. Courses for which the user has met prerequisites (eligible courses).
2. Courses fulfilling college distribution requirements (overlapping courses).
3. Courses satisfying requirements for other selected major(s) and minor(s) (overlapping courses).
4. Courses with lower workload/difficulty (CUReview data) (in development).
5. Courses with higher instructor ratings (Rate My Professor data) (in development).

Users can customize ranking preferences using a filter button on the web page.

## Technology Stack  

| Component    | Technology Used |
|-------------|----------------|
| **Data Collection** | Web scraping from **Cornell’s Class Roster** (`get.py`) |
| **Backend** | Python with **Flask** (`app.py`) |
| **Frontend** | JavaScript, HTML, and CSS (see `templates` and `static` folders) |
| **Helper Functions** | Located in `course.py`, `importance.py`, `level.py`, etc. |

README Latest update: January 30, 2025