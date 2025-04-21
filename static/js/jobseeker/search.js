
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('jobSearchForm');
    const resultsDiv = document.getElementById('job-details');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const jobTitle = document.getElementById('jobTitle').value.trim();
        const location = document.getElementById('location').value.trim();  // Location input

        if (!jobTitle) {  
            resultsDiv.innerHTML = "<p>Please enter a job title.</p>";
            return;
        }

        try {   
            // Construct API URL dynamically
            let apiUrl = `/api/search/?q=${encodeURIComponent(jobTitle)}`;
            if (location) {
                apiUrl += `&p=${encodeURIComponent(location)}`;
            }

            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error(`Error fetching jobs: ${response.status}`);

            const apiResposeData = await response.json();

            if (apiResposeData.jobs.length === 0) {
                resultsDiv.innerHTML = "<p>No jobs found.</p>";
                return;
            }
            const jobsHTML = apiResposeData.jobs.map(job => `
        <a href="/job/?r=${ job.slug }" target="_blank" class="job-description">
            <div class="job-card">
                <div class="job-header">
                    <div>
                        <h2>${ job.title }</h2>
                        <p class="company-name">${ job.company }</p>
                    </div>
                    ${job.is_applied 
                    ? `<div onclick="window.location='./../status/applied';" class="view-job">View status</div>` 
                    : `<div class="apply-job">Apply</div>`
                    }


                </div>
        
                <div class="job-details">
                    <p class="details-row">
                        <span><i class="fas fa-map-marker-alt"></i>
                            ${ job.location_id.length != 0 ? job.location_id : 'Not disclosed'}
                        </span>
                        <span><i class="fa fa-briefcase"></i>
                            ${job.min_experience !== job.max_experience ? `${job.min_experience!== null?job.min_experience:'Not disclosed'} - ${job.max_experience!== null?job.max_experience:'Not disclosed'}` : job.max_experience !== null?job.max_experience:'Not disclosed'} Years

                            </span>
                      </p>
                      <p class="details-row">
                        <span><i class="fas fa-clock"></i>${ job.employment_type != null ? job.employment_type : 'Not disclosed' }</span>
                        <span><i class="fa fa-indian-rupee-sign"></i><span class="salary" data-salary="${ job.salary }"></span></span>
                        <span><i class="fa fa-graduation-cap"></i>${ job.qualifications.length != 0 ? job.qualifications : 'Not disclosed' }</span>
                        <span><i class="fa fa-laptop"></i>  
                        <span class="work-type"
                            data-onsite="${ job.is_onsite}"
                            data-wfh="${ job.is_work_from_home}"
                            data-hybrid="${ job.is_hybrid}"
                        ></span>                        
                        </span>
                      </p>
                    <div class="skills skills-container" data-skills="${job.skills}">
                    </div>
                    

                    <p3 class="description">
                        ${ job.description }
                    </p3>
                </div>
        
                <div class="job-footer">
                    <span class="time-since">${ timeSince(job.refreshed_date) }</span>

                    <span>${ job.opening_count !== null ? job.opening_count : '' } Openings</span>
                    <span>${ job.applied_count } Applied</span>
                    <form method="POST" action="/bookmark/">
                        
                        <input type="hidden" value="${ job.slug }" name="slug">
                        <input type="checkbox" id="save" class="bookmark-checkbox" ${ job.is_saved ? 'checked' : '' }>
                        <label for="save">
                            <button type="submit" class="save_job" name="save_job"><i class="fas fa-bookmark bookmark-icon"></i><span class="save-text">${ job.is_saved ? 'Saved' : 'Save' }<span></button>
                            
                        </label>
                    </form>
                    
                </div>
            </div>
            </a>
                `).join('') 
   
//             // Build the pagination HTML
//             const paginationHTML = apiResposeData.pagination.map(page => `
//                 <button class="pagination-button" data-page="${page.number}">
//                     ${page.number}
//                 </button>
//             `).join('');

                // Build pagination HTML using correct fields
                const pagination = apiResposeData.pagination;

                let paginationHTML = `<div class="pagination">`;
                // Previous button
                if (pagination.has_previous) {
                    paginationHTML += `<a href="?q=${jobTitle}&p=${location}&page=${pagination.current_pages - 1}">Previous</a>`;
                }
                // Page numbers
                for (let num = 1; num <= pagination.total_pages; num++) {
                    if (num === pagination.current_pages) {
                        paginationHTML += `<span class="current">${num}</span>`;
                    } else if (num > pagination.current_pages - 3 && num < pagination.current_pages + 3) {
                        paginationHTML += `<a href="?q=${jobTitle}&p=${location}&page=${num}">${num}</a>`;
                    } else if (num === 1 || num === pagination.total_pages) {
                        paginationHTML += `<a href="?q=${jobTitle}&p=${location}&page=${num}">${num}</a>`;
                    } else if (num === pagination.current_pages - 4 || num === pagination.current_pages + 4) {
                        paginationHTML += `<span>...</span>`;
                    }
                }

                // Next button
                if (pagination.has_next) {
                    paginationHTML += `<a href="?q=${jobTitle}&p=${location}&page=${pagination.current_pages + 1}" class="last">Next</a>`;
                }
                paginationHTML += `</div>`;

                // Total jobs summary
                const summaryHTML = `
                    <span class="total-jobs">
                        ${pagination.page_from} - ${pagination.page_to} of ${pagination.page_of} 
                        <strong>${apiResposeData.keyword1}</strong> Jobs
                    </span>
                `;

                // Combine and inject into the page
                resultsDiv.innerHTML = summaryHTML + jobsHTML + paginationHTML;

                workTypeFunc();
                keyskills();
                salaryInLPA();


        } catch (error) {
            console.error("Error fetching jobs:", error);
            resultsDiv.innerHTML = "<p>Something went wrong. Please try again later.</p>";
        }
    });
});


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

document.addEventListener("DOMContentLoaded", function() {
    updateTimeSince();
    workTypeFunc();
    keyskills();
    salaryInLPA();
});
