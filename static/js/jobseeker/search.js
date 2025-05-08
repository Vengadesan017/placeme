/**
 * ===========================================================
 * Job Search Page Scripts
 * ===========================================================
 * This script powers the dynamic job search UI including:
 * 
 * --> Collecting selected filters from checkboxes and sliders
 * --> Building dynamic GET request URLs for job search API
 * --> Fetching and rendering job listings based on filters
 * --> Dynamically populating and updating filter options
 * --> Debounced filtering to optimize performance
 * --> Rendering pagination and user-interactive job cards
 * --> Managing filter reset and UI re-binding
 * 
 * Main Functions:
 * - getSelectedFilters()       → Collects all active filters
 * - attachFilterListeners()    → Adds change listeners to filters
 * - populateFilters()          → Dynamically renders filter options
 * - renderJobs()               → Displays job cards and pagination
 * - debounce()                 → Limits rapid fetch triggers
 * - fetchJobs()                → Main fetch logic and UI update
 * 
 * Events:
 * - DOMContentLoaded           → Attaches listeners on page load
 * 
 * Dependencies:
 * - HTML structure (with correct class & ID usage)
 * - CSS for rendering job cards & filters correctly
 * - Server API endpoint at /api/search/
 */


// Function to load the filter data in URL for get fetch call
function getSelectedFilters() {
    const params = new URLSearchParams();

    // Work Mode
    document.querySelectorAll('input[name="work_mode"]:checked').forEach(el => {
        params.append('work_mode', el.value);
    });

    // Experience (single value from slider)
    const experience = document.getElementById('experienceSlider').value;
    if (experience !== "-1") {
        params.append('experience', experience);
    }

    // Salary
    document.querySelectorAll('input[name="salary"]:checked').forEach(el => {
        params.append('salary', el.value);
    });

    // Organization Type
    document.querySelectorAll('input[name="organization_type"]:checked').forEach(el => {
        params.append('organization_type', el.value);
    });

    // Employment Type
    document.querySelectorAll('input[name="employment_type"]:checked').forEach(el => {
        params.append('employment_type', el.value);
    });

    // Qualification
    document.querySelectorAll('input[name="qualification"]:checked').forEach(el => {
        params.append('qualification', el.value);
    });

    // Industry Type
    document.querySelectorAll('input[name="industry_type"]:checked').forEach(el => {
        params.append('industry_type', el.value);
    });

    // Location from filter checkboxes
    document.querySelectorAll('input[name="location"]:checked').forEach(el => {
        params.append('location', el.value);
    });

    return params;
}

// Function to re-bind filter change events 
//  used to call the fetch method when chances mad in filter option
// and rebind when after the fetch call
function attachFilterListeners() {
    const filterInputs = document.querySelectorAll('.filter-container input[type="checkbox"], #experienceSlider');
    filterInputs.forEach(input => {
        input.addEventListener('change', () => {
            console.log("Filter updated, fetching jobs...");
            debouncedFetchJobs();
        });
    });
}



// Function For update the filter based on fetch call method ( After API call )
function populateFilters(filters, experienceValue = "-1") {
    const filterContainer = document.querySelector('.filter-container');

    if (!filters || typeof filters !== 'object') {
        console.warn("No filters data available.");
        if (filterContainer) {
            filterContainer.style.display = 'none';
        }
        return;
    } else {
        if (filterContainer) {
            filterContainer.style.display = 'block';
        }
    }

    const filterMap = {
        work_mode: "moreWorOptions",
        employment_type: "moreCatOptions",
        salary: "moreSalOptions",
        qualification: "moreEduOptions",
        industry_type: "moreIndOptions",
        organization_type: "moreComOptions",
        location: "moreLocOptions"
    };

    for (const [filterKey, elementId] of Object.entries(filterMap)) {
        const container = document.getElementById(elementId);
        const filterData = filters[filterKey];

        if (!container) continue;

        const previouslySelected = new Set(
            Array.from(container.querySelectorAll(`input[name="${filterKey}"]:checked`)).map(input => input.value)
        );

        container.innerHTML = ""; // Clear old options

        if (filterData && typeof filterData === 'object') {
            Object.entries(filterData).forEach(([label, count]) => {
                if (count > 0) {
                    const isChecked = previouslySelected.has(label) ? 'checked' : '';
                    const checkbox = document.createElement("label");
                    checkbox.innerHTML = `
                        <input type="checkbox" name="${filterKey}" value="${label}" ${isChecked}>
                        ${label} (${count})
                    `;
                    container.appendChild(checkbox);
                }
            });
        }
    }

    // Restore experience value
    const experienceSlider = document.getElementById('experienceSlider');
    if (experienceSlider) {
        const min = parseInt(experienceSlider.min, 10);
        const value = parseInt(experienceValue, 10);
        if (!isNaN(value) && value >= min) {
            experienceSlider.value = value;
        } else {
            experienceSlider.value = min; // fallback to min if invalid
        }

        experienceSlider.value = experienceValue;
        updateExperienceLabel(experienceValue);
    }

    //  Re-attach listeners after dynamic filters are rendered
    attachFilterListeners();
}


// Function for update the job cards with pagination
function renderJobs(apiResposeData, resultsDiv ) {
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
                    <p class="details-row details-row-2">
                        <span><i class="fas fa-map-marker-alt"></i>
                            ${ job.location_id.length != 0 ? job.location_id : 'Not disclosed'}
                        </span>
                        <span><i class="fa fa-briefcase"></i>
                            ${job.min_experience !== job.max_experience ? `${job.min_experience!== null?job.min_experience:'Not disclosed'} - ${job.max_experience!== null?job.max_experience:'Not disclosed'}` : job.max_experience !== null?job.max_experience:'Not disclosed'} Years

                            </span>
                    </p>
                    <p class="details-row details-row-4">
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
                    


                </div>
        
                <div class="job-footer">
                    <span class="time-since">${ timeSince(job.refreshed_date) }</span>

                    <span>${ job.opening_count !== null ? job.opening_count : '' } Openings</span>
                    ${ job.applied_count > 10 ? `<span>${ job.applied_count } Applicants</span>` : '' }
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
    
}


// remove the filter from the Browser URL
function clearFiltersFromBrowser(){
    // Remove all query parameters except 'p' and 'q'
    const currentUrl = new URL(window.location.href);
    const params = currentUrl.searchParams;

    // Store values of 'p' and 'q'
    const keepParams = ['q', 'p'];
    const preservedValues = {};
    keepParams.forEach(param => {
        if (params.has(param)) {
            preservedValues[param] = params.get(param);
        }
    });

    // Clear all search params
    currentUrl.search = '';

    // Restore only 'p' and 'q'
    for (const [key, value] of Object.entries(preservedValues)) {
        currentUrl.searchParams.set(key, value);
    }

    // Update the browser URL
    window.history.pushState({}, '', currentUrl.toString());
}
// Function for fetchJobs() only runs once after a small delay (e.g. 300 ms), 
// even if multiple changes happen quickly
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}
const debouncedFetchJobs = debounce(fetchJobs, 300);

// fetch method to get the data from server 
async function fetchJobs() {
    const jobTitle = document.getElementById('jobTitle').value.trim();
    const location = document.getElementById('location').value.trim();
    const resultsDiv = document.getElementById('job-details');

    if (!jobTitle) {
        resultsDiv.innerHTML = "<p>Please enter a job title.</p>";
        return;
    }

    try {
        let apiUrl = `/api/search/?q=${encodeURIComponent(jobTitle)}`;
        if (location) {
            apiUrl += `&p=${encodeURIComponent(location)}`;
        }

        // Collect all selected filters
        const filters = ['work_mode', 'employment_type', 'salary', 'qualification', 'industry_type', 'organization_type', 'location'];
        filters.forEach(filter => {
            document.querySelectorAll(`input[name="${filter}"]:checked`).forEach(checkbox => {
                apiUrl += `&${filter}=${encodeURIComponent(checkbox.value)}`;
            });
        });

        // Add the experience filter value
        const experienceSlider = document.getElementById('experienceSlider');
        if (experienceSlider && experienceSlider.value !== "-1") {
            apiUrl += `&experience=${encodeURIComponent(experienceSlider.value)}`;
        }

        // Update the browser URL
        window.history.pushState({ path: apiUrl }, '', apiUrl.replace('/api', ''));

        console.log("Fetching jobs with URL: ", apiUrl);
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error(`Error fetching jobs: ${response.status}`);

        const apiResponseData = await response.json();

        if (apiResponseData.jobs.length === 0) {
            resultsDiv.innerHTML = "<p>No jobs found.</p>";
        } else {
            renderJobs(apiResponseData, resultsDiv);
        }

        // Pass the experience slider value so it can be restored
        const sliderValue = experienceSlider ? experienceSlider.value : "-1";
        populateFilters(apiResponseData.filters, sliderValue);

    } catch (error) {
        console.error("Error fetching jobs:", error);
        resultsDiv.innerHTML = "<p>Something went wrong. Please try again later.</p>";
    }
}

// Initial setup after page load
// Update event listeners for button and all filters action to call the fetch method
document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.querySelector('.search-button');
    const clearButton = document.querySelector('.clear-filters-button');
    const experienceSlider = document.getElementById('experienceSlider');

    // Attach event to search button
    if (searchButton) {
        searchButton.addEventListener('click', fetchJobs);
    }

    // Attach filter listeners (checkboxes and experience slider)
    attachFilterListeners();

    // Clear filters and trigger a fresh search
    if (clearButton) {
        clearButton.addEventListener('click', () => {
            console.log("Clearing all filters...");

            // Uncheck all filter checkboxes
            document.querySelectorAll('.filter-container input[type="checkbox"]').forEach(input => {
                input.checked = false;
            });

            // Reset experience slider
            if (experienceSlider) {
                experienceSlider.value = -1;
                experienceSlider.setAttribute('data-prev', -1);
                updateExperienceLabel(-1);
            }

            // Clear filter from browser URL bar
            clearFiltersFromBrowser();

            // Fetch jobs with cleared filters
            debouncedFetchJobs();
        });
    }
});




    // 
    // 
    // 
    // 
    // 
    // 
    // 
    // 
    // Fetch call using the button click event Only
    // 
    // 
    // 
    // 
    // 
    // 
// Function to load the filter data in URL for get fetch call
// function getSelectedFilters() {
//     const params = new URLSearchParams();

//     // Work Mode
//     document.querySelectorAll('input[name="work_mode"]:checked').forEach(el => {
//         params.append('work_mode', el.value);
//     });

//     // Experience (single value from slider)
//     const experience = document.getElementById('experienceSlider').value;
//     if (experience !== "-1") {
//         params.append('experience', experience);
//     }

//     // Salary
//     document.querySelectorAll('input[name="salary"]:checked').forEach(el => {
//         params.append('salary', el.value);
//     });

//     // Organization Type
//     document.querySelectorAll('input[name="organization_type"]:checked').forEach(el => {
//         params.append('organization_type', el.value);
//     });

//     // Employment Type
//     document.querySelectorAll('input[name="employment_type"]:checked').forEach(el => {
//         params.append('employment_type', el.value);
//     });

//     // Qualification
//     document.querySelectorAll('input[name="qualification"]:checked').forEach(el => {
//         params.append('qualification', el.value);
//     });

//     // Industry Type
//     document.querySelectorAll('input[name="industry_type"]:checked').forEach(el => {
//         params.append('industry_type', el.value);
//     });

//     // Location from filter checkboxes
//     document.querySelectorAll('input[name="location"]:checked').forEach(el => {
//         params.append('location', el.value);
//     });

//     return params;
// }

// // Function to clear the filter data 
// document.addEventListener('DOMContentLoaded', () => {
//     const clearButton = document.querySelector('.clear-filters-button');

//     clearButton.addEventListener('click', () => {
//         // Uncheck all filter checkboxes
//         document.querySelectorAll('.filter-container input[type="checkbox"]').forEach(input => {
//             input.checked = false;
//         });

//         // Reset experience slider
//         const experienceSlider = document.getElementById('experienceSlider');
//         if (experienceSlider) {
//             experienceSlider.value = -1;
//             experienceSlider.setAttribute('data-prev', -1);
//             updateExperienceLabel(-1); // Update label text
//         }

//         // Optionally, trigger a new search with no filters
//         document.querySelector('.search-button').click();
//     });
// });
// // Detect form submission and make the fetch call
// document.addEventListener('DOMContentLoaded', () => {
//     const searchButton = document.querySelector('.search-button');


//     searchButton.addEventListener('click', async () => {

//         const jobTitle = document.getElementById('jobTitle').value.trim();
//         const location = document.getElementById('location').value.trim();  // Location input
//         const resultsDiv = document.getElementById('job-details');
//         if (!jobTitle) {  
//             resultsDiv.innerHTML = "<p>Please enter a job title.</p>";
//             return;
//         }

//         try {   
//             // Base params
//             const params = new URLSearchParams();
//             params.append('q', jobTitle);
//             if (location) params.append('p', location);

//             // Add selected filter params
//             const filterParams = getSelectedFilters();
//             for (const [key, value] of filterParams.entries()) {
//                 params.append(key, value);
//             }
//             // Construct API URL dynamically
//             const apiUrl = `/api/search/?${params.toString()}`;

//             // Update URL in browser bar
//             const newUrl = `/search/?${params.toString()}`;
//             window.history.pushState({ path: newUrl }, '', newUrl);

//             const response = await fetch(apiUrl);
//             if (!response.ok) throw new Error(`Error fetching jobs: ${response.status}`);

//             const apiResposeData = await response.json();

//             if (apiResposeData.jobs.length === 0) {
//                 resultsDiv.innerHTML = "<p>No jobs found.</p>";
//                 populateFilters(apiResposeData.filters);
//                 return;
//             }
//             renderJobs(apiResposeData, resultsDiv );
//             const experienceSlider = document.getElementById('experienceSlider');
//             const previousExperienceValue = experienceSlider?.value || "-1";
            
//             populateFilters(apiResposeData.filters, previousExperienceValue);


//         } catch (error) {
//             console.error("Error fetching jobs:", error);
//             resultsDiv.innerHTML = "<p>Something went wrong. Please try again later.</p>";
//         }
//     });
// });