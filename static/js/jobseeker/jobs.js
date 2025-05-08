/**
 * ===========================================================
 * Job Card Enhancements: Display Helpers & Post-processing 
 * Filter Enhancement: View more & experience slider & Search in location
 * ===========================================================
 * This script enhances rendered job cards by formatting:
 * 
 * 📅 Posted date → Converts raw timestamps to "X time ago"
 * 🏢 Work type   → Shows job location type (Onsite / WFH / Hybrid)
 * 🛠️  Skills      → Renders comma-separated skills as styled tags
 * 💰 Salary      → Converts and formats salary to "LPA" (Lakhs Per Annum)
 * 
 * Main Functions:
 * - timeSince(postedDate)      → Returns human-readable "time ago"
 * - updateTimeSince()          → Updates all `.time-since` elements
 * - workTypeFunc()             → Sets readable work mode from data attributes
 * - keyskills()                → Converts string of skills into span tags
 * - salaryInLPA()              → Converts raw salary to LPA format
 * 
 * Execution:
 * - All enhancements are run inside DOMContentLoaded
 *   to ensure job cards exist in the DOM before processing
 * 
 * This script enhances filters:
 * 
 */


    // Function to update the experience slider
    function updateExperienceLabel(value) {
        const experienceLabel = document.getElementById('experienceLabel');
        const slider = document.getElementById('experienceSlider');
    
        // Set label text, with 20+ years if at max
        experienceLabel.textContent = value === '21' ? '20+' : value === '-1' ? 'Any' : `${value} `;
    
        // Position label above the slider thumb
        const thumbPosition = ((parseInt(value, 10) + 1) / 22) * 100;
        // experienceLabel.style.left = `calc(${thumbPosition}% - 10px)`;
        experienceLabel.style.left = `calc(${thumbPosition}% + 10px)`;
    
        // Update the background fill as the slider moves
        slider.style.setProperty('--progress', `${thumbPosition}%`);
    }
    
    // Function for view more option in overflow data in filters
    function toggleView(containerId, toggleButtonId) {
        const container = document.getElementById(containerId);
        const toggleButton = document.getElementById(toggleButtonId);
    
        if (container && toggleButton) {
            if (container.style.maxHeight === "120px" || container.style.maxHeight === "") {
                container.style.maxHeight = "400px";
                container.style.overflow = "auto";
                toggleButton.textContent = "View Less";
            } else {
                container.style.maxHeight = "120px";
                container.style.overflow = "hidden";
                toggleButton.textContent = "View More";
            }
        } else {
            console.error("Container or Toggle Button not found.");
        }
    }
    // Search bar in location filter
    function filterSearchLocation() {
        var input, filter, ul, labels, i, txtValue;
        input = document.getElementById("filterLocation");
        filter = input.value.toUpperCase();
        ul = document.getElementById("moreLocOptions");
        labels = ul.getElementsByTagName("label");
    
        for (i = 0; i < labels.length; i++) {
            txtValue = labels[i].textContent || labels[i].innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                labels[i].style.display = "";
            } else {
                labels[i].style.display = "none";
            }
        }
    }

    // for function in for jobs cards posted date
    function timeSince(postedDate) {
        let postedTime = new Date(postedDate);
        let now = new Date();
        let seconds = Math.floor((now - postedTime) / 1000);

        let intervals = {
            "year": 31536000,
            "month": 2592000,
            "week": 604800,
            "day": 86400,
            "hour": 3600,
            "minute": 60,
        };

        for (let [unit, value] of Object.entries(intervals)) {
            let interval = Math.floor(seconds / value);
            if (interval >= 1) {
                return `${interval} ${unit}${interval !== 1 ? "s" : ""} ago`;
            }
        }
        return "Just now";
    }

    function updateTimeSince() {
        document.querySelectorAll(".time-since").forEach(span => {
            let postedDate = span.getAttribute("data-posted-date"); 
            if (postedDate) {
                span.innerText = timeSince(postedDate);
            }
        });
    }


    // work type 
    function workTypeFunc() {
        document.querySelectorAll(".work-type").forEach(span => {
            let isOnsite = span.getAttribute("data-onsite") === "true";
            let isWFH = span.getAttribute("data-wfh") === "true";
            let isHybrid = span.getAttribute("data-hybrid") === "true";

            let workTypes = [];
            if (isOnsite) workTypes.push("Onsite");
            if (isWFH) workTypes.push("Work from Home");
            if (isHybrid) workTypes.push("Hybrid");
            if(workTypes.length !== 0){
                span.innerText = workTypes.join(", ");
            }
            else{
                span.innerText = `Not disclosed`
            }

        });
    }

    // skills 
    function keyskills() {

        document.querySelectorAll(".skills-container").forEach(skillsContainer => {
            let skillsString = skillsContainer.getAttribute("data-skills"); // Get the string from data attribute

        
            if (skillsString) {
                let skillsArray = skillsString.split(","); // Convert to array
                skillsArray.forEach(skill => {
                    let skillSpan = document.createElement("span");
                    skillSpan.className = "key-skills";
                    skillSpan.innerText = skill.trim(); // Remove extra spaces
                    skillsContainer.appendChild(skillSpan);
                });
            } else {
                let noSkillSpan = document.createElement("span");
                noSkillSpan.className = "key-skills";
                noSkillSpan.innerText = "No skills provided";
                skillsContainer.appendChild(noSkillSpan);
            }
        });

    }

    // Salary 
    function salaryInLPA(){
        document.querySelectorAll(".salary").forEach(salarySpan => {
            let salary = salarySpan.getAttribute("data-salary");

            if (salary && salary!="None" && salary != "null") {
                let salaryLPA = parseFloat(salary) / 100000; // Convert to LPA
                let formattedSalary = salaryLPA % 1 === 0 ? salaryLPA.toFixed(0) : salaryLPA.toFixed(1); // Remove .00, keep .5

                salarySpan.innerHTML = `${formattedSalary} LPA`;
            }
            else{
                salarySpan.innerHTML = `Not disclosed`;
            }
        });
    }


    // functions are executed only after the HTML document has been fully loaded and parsed, 
    // but before stylesheets, images, and subframes are completely loaded
    document.addEventListener("DOMContentLoaded", function() {
        updateTimeSince();
        workTypeFunc();
        keyskills();
        salaryInLPA();
    });





// function filterJobs() {
//     const jobCards = document.querySelectorAll('.job-card');
//     const workModeFilters = getSelectedFilters('workMode');
//     const experienceFilters = getSelectedFilters('experience');
//     const salaryFilters = getSelectedFilters('salary');
//     const departmentFilters = getSelectedFilters('department');
//     const companyTypeFilters = getSelectedFilters('companyType');
//     const roleCategoryFilters = getSelectedFilters('roleCategory');
//     const locationFilters = getSelectedFilters('location');

//     jobCards.forEach(card => {
//         const workMode = card.querySelector('.job-details').textContent.toLowerCase();
//         const location = card.querySelector('.job-details').textContent.toLowerCase();

//         let show = true;

//         if (workModeFilters.length && !workModeFilters.some(filter => workMode.includes(filter))) {
//             show = false;
//         }

//         if (locationFilters.length && !locationFilters.some(filter => location.includes(filter))) {
//             show = false;
//         }

//         if (show) {
//             card.style.display = 'block';
//         } else {
//             card.style.display = 'none';
//         }
//     });
// }

// function getSelectedFilters(filterName) {
//     const checkboxes = document.querySelectorAll(`input[name="${filterName}"]:checked`);
//     return Array.from(checkboxes).map(checkbox => checkbox.value.toLowerCase());
// }

// document.querySelector('button').addEventListener('click', filterJobs);

