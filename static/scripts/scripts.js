async function changeNumber() {
    const response = await fetch('/change_number', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    });
    if (response.ok) {
        const updatedNumber = await response.json();
        console.log('Updated Number:', updatedNumber);
    }
}

async function markCourseAsTakenA(course) {
    try {
        const response = await fetch('/add_course_taken', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ course: course })
        });

        if (response.ok) {
            const updatedCourses = await response.json();
            console.log('Courses Taken:', updatedCourses);

            // Update the sidebar
            const sideBar = document.querySelector('.side-bar .course-grid-S');
            sideBar.innerHTML = '';
            updatedCourses.forEach(course => {
                const courseItem = document.createElement('div');
                courseItem.classList.add('course-item');
                courseItem.id = `course-item-${course}`;
                courseItem.innerHTML = `
                    <button class="remove-course" onclick="removeCourse('${course}')">✖</button>
                    <span class="course-name">${course}</span>
                `;
                sideBar.appendChild(courseItem);
            });

            // Update the course block appearance on the main page
            const courseBlocksA = document.querySelectorAll('.course-block-A');
            for (const block of courseBlocksA) {
                const courseCode = block.querySelector('button').textContent.trim();

                if (updatedCourses.includes(courseCode)) {
                    block.querySelector('button').classList.add('taken-course-A');
                    block.querySelector('button').classList.remove('eligible-course-A');
                    block.querySelector('button').classList.remove('default-course-A');
                } else {
                    // Check eligibility for each course
                    const eligible = await checkEligibility(courseCode);
                    if (eligible) {
                        block.querySelector('button').classList.add('eligible-course-A');
                        block.querySelector('button').classList.remove('taken-course-A');
                        block.querySelector('button').classList.remove('default-course-A');
                    } else {
                        block.querySelector('button').classList.add('default-course-A');
                        block.querySelector('button').classList.remove('taken-course-A');
                        block.querySelector('button').classList.remove('eligible-course-A');
                    }
                }
            }

            // Update the group-taken class for the course's parent group
            const courseGroup = document.getElementById(`button-${course}`).closest('.course-group');
            if (courseGroup) {
                courseGroup.classList.add('group-taken'); // Add 'group-taken' class
            }
        } else {
            console.error('Failed to add course:', course);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function markCourseAsTakenB(course,sanitizedSectionName) {
    try {
        const response = await fetch('/add_course_taken', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ course: course })
        });

        if (response.ok) {
            const updatedCourses = await response.json();
            console.log('Courses Taken:', updatedCourses);

            // Update the sidebar
            const sideBar = document.querySelector('.side-bar .course-grid-S');
            sideBar.innerHTML = '';
            updatedCourses.forEach(course => {
                const courseItem = document.createElement('div');
                courseItem.classList.add('course-item');
                courseItem.id = `course-item-${course}`;
                courseItem.innerHTML = `
                    <button class="remove-course" onclick="removeCourse('${course}')">✖</button>
                    <span class="course-name">${course}</span>
                `;
                sideBar.appendChild(courseItem);
            });

            // update the course list
            addCourseInCourseListB(course,sanitizedSectionName);
            incrementCountB(sanitizedSectionName)
            updateEligibilityB(sanitizedSectionName, updatedCourses)
        } else {
            console.error('Failed to add course:', course);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function addCourseInCourseListB(courseName, sanitizedSectionName) {
    // Get the container where the button should be added
    const courseList = document.getElementById(`course-list-${sanitizedSectionName}`);
    
    // Create a new <button> element
    const button = document.createElement('button');
    button.className = 'taken-course-B'; // Add the same class as other buttons
    button.textContent = courseName;  // Set the button text
    
    // Optionally, wrap the button in a link (<a>)
    const link = document.createElement('a');
    link.href = courseName;          // Set the link URL (example: course name as link)
    link.target = '_blank';          // Open in a new tab
    link.appendChild(button);        // Add the button inside the link
    
    // Add the button (or the link with the button) to the container
    courseList.appendChild(link);
}

function coursesInGridB(sanitizedSectionName) {
    // Get the parent container for the course grid
    const courseGrid = document.getElementById(`course-gridB-${sanitizedSectionName}`);
    
    if (!courseGrid) {
        console.error(`Element with id course-gridB-${sanitizedSectionName} not found.`);
        return [];
    }

    // Find only the buttons associated with courses (exclude .taken-btn-B)
    const courseButtons = courseGrid.querySelectorAll('.course-block-B > a > button');

    // Log or return the course buttons
    return courseButtons;
}

async function updateEligibilityB(sanitizedSectionName, updatedCourses) {
    const courseButtons = coursesInGridB(sanitizedSectionName);

    for (const courseButton of courseButtons) {
        const courseCode = courseButton.textContent.trim();

        if (updatedCourses.includes(courseCode)) {
            // Mark the course as taken
            courseButton.classList.add('taken-course-B');
            courseButton.classList.remove('eligible-course-B');
            courseButton.classList.remove('default-course-B');
        } else {
            // Check eligibility asynchronously
            const eligible = await checkEligibility(courseCode);
            if (eligible) {
                // Mark as eligible
                courseButton.classList.add('eligible-course-B');
                courseButton.classList.remove('taken-course-B');
                courseButton.classList.remove('default-course-B');
            } else {
                // Mark as default
                courseButton.classList.add('default-course-B');
                courseButton.classList.remove('taken-course-B');
                courseButton.classList.remove('eligible-course-B');
            }
        }
    }
}

function incrementCountB(sanitizedSectionName) {
    // Find the counter element
    const counter = document.getElementById(`taken-counter-${sanitizedSectionName}`);
    if (!counter) {
        console.error(`Counter for section ${sanitizedSectionName} not found.`);
        return;
    }

    // Increment the counter
    const currentCount = parseInt(counter.textContent, 10); // Get the current number
    counter.textContent = currentCount + 1; // Increment the number
}

function decrementCount(sanitizedSectionName) {
    const counter = document.getElementById(`taken-counter-${sanitizedSectionName}`);
    if (!counter) {
        console.error(`Counter for section ${sanitizedSectionName} not found.`);
        return;
    }

    const currentCount = parseInt(counter.textContent, 10);
    counter.textContent = Math.max(currentCount - 1, 0); // Ensure count doesn't go below 0
}

async function removeCourse(course) {
    try {
        const response = await fetch('/remove_course_taken', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ course: course })
        });

        if (response.ok) {
            const updatedCourses = await response.json();
            console.log('Updated Courses Taken:', updatedCourses);

            // Remove the course-item from the sidebar
            const courseItem = document.getElementById(`course-item-${course}`);
            if (courseItem) {
                courseItem.remove();
            }

            // Update the course block appearance on the main page
            const courseBlocksA = document.querySelectorAll('.course-block-A');
            for (const block of courseBlocksA) {
                const courseCode = block.querySelector('button').textContent.trim();
                const button = block.querySelector('button');

                if (!updatedCourses.includes(courseCode)) {
                    // Remove 'taken-course-A' class
                    button.classList.remove('taken-course-A');

                    // Check eligibility dynamically
                    const eligible = await checkEligibility(courseCode);
                    if (eligible) {
                        button.classList.add('eligible-course-A');
                        button.classList.remove('default-course-A');
                    } else {
                        button.classList.add('default-course-A');
                        button.classList.remove('eligible-course-A');
                    }
                }
            }

            // Update the 'group-taken' class for the course's parent group
            const courseGroup = document.getElementById(`button-${course}`)?.closest('.course-group');
            if (courseGroup) {
                const courseButtonsInGroup = courseGroup.querySelectorAll('.course-block-A button');
                const hasTakenCourses = Array.from(courseButtonsInGroup).some(button =>
                    button.classList.contains('taken-course-A')
                );

                if (!hasTakenCourses) {
                    courseGroup.classList.remove('group-taken');
                }
            }

            // Optionally, update the counter for the section
            const courseLists = document.querySelectorAll('.course-list-B');
            const sectionId = Array.from(courseLists).find(list =>
                Array.from(list.querySelectorAll('button')).some(btn => btn.textContent.trim() === course)
            )?.id;
            const sanitizedSectionName = sectionId.replace('course-list-', '')
            if (sectionId) {
                console.log(`Section ID for course "${course}": ${sectionId}`);
                decrementCount(sanitizedSectionName);
            }

            // Find and remove the course in the corresponding course-list-B
            for (const courseList of courseLists) {
                const courseButton = Array.from(courseList.querySelectorAll('button')).find(
                    btn => btn.textContent.trim() === course
                );

                if (courseButton) {
                    console.log(`Removing course "${course}" from section: ${courseList.id}`);
                    courseButton.parentElement.remove(); // Remove the parent <a> containing the button
                    break; // Exit loop once the course is found
                }
            }
            updateEligibilityB(sanitizedSectionName, updatedCourses)

        } else {
            console.error('Failed to remove course:', course);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function checkEligibility(course) {
    try {
        const response = await fetch('/check_eligibility', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ course: course })
        });

        if (response.ok) {
            const data = await response.json();
            return data.is_eligible; // Returns true or false
        } else {
            console.error('Failed to check eligibility for course:', course);
            return false;
        }
    } catch (error) {
        console.error('Error checking eligibility:', error);
        return false;
    }
}

function reloadPage() {
    console.log("Saving scroll position and reloading...");

    // Save the scroll position of the major-requirement container
    const majorRequirement = document.querySelector('.major-requirement');
    if (majorRequirement) {
        localStorage.setItem('scrollPosition', majorRequirement.scrollTop);
    }

    // Reload the page
    location.reload();
}

window.addEventListener('load', () => {
    const majorRequirement = document.querySelector('.major-requirement');
    const scrollPosition = localStorage.getItem('scrollPosition');

    if (majorRequirement && scrollPosition) {
        console.log(`Restoring scroll position for major-requirement to: ${scrollPosition}`);
        majorRequirement.scrollTop = parseInt(scrollPosition, 10); // Restore the scroll position
        localStorage.removeItem('scrollPosition'); // Clean up
    }
});

document.addEventListener("DOMContentLoaded", function () {
    console.log("Initializing pagination...");

    const sectionStates = {};

    document.querySelectorAll("[data-section]").forEach(courseGrid => {
        const sanitizedSectionName = courseGrid.dataset.section;

        const courseBlocks = Array.from(courseGrid.querySelectorAll(".course-block-B"));
        console.log(`Number of courses in section "${sanitizedSectionName}": ${courseBlocks.length}`);

        const itemsPerPage = 12;
        const totalPages = Math.ceil(courseBlocks.length / itemsPerPage);

        sectionStates[sanitizedSectionName] = {
            currentPage: 1,
            totalPages: totalPages,
            courseBlocks: courseBlocks,
        };

        console.log(`Total pages for section "${sanitizedSectionName}": ${totalPages}`);
        renderPage(sanitizedSectionName);
    });

    function renderPage(sectionName) {
        const { currentPage, totalPages, courseBlocks } = sectionStates[sectionName];
        const itemsPerPage = 12; // Define the number of items per page locally
        courseBlocks.forEach((block, index) => {
            block.style.display =
                index >= (currentPage - 1) * itemsPerPage && index < currentPage * itemsPerPage
                    ? "block"
                    : "none";
        });

        const paginationControls = document.getElementById(`pagination-controls-${sectionName}`);

        paginationControls.querySelector("button:first-child").disabled = currentPage === 1;
        paginationControls.querySelector("button:last-child").disabled = currentPage === totalPages;
    }

    window.changePage = function (sectionName, direction) {
        const sectionState = sectionStates[sectionName];
        sectionState.currentPage += direction;

        if (sectionState.currentPage < 1) sectionState.currentPage = 1;
        if (sectionState.currentPage > sectionState.totalPages) sectionState.currentPage = sectionState.totalPages;

        renderPage(sectionName);
    };
});