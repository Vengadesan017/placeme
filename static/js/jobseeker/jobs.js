
function filterJobs() {
    const jobCards = document.querySelectorAll('.job-card');
    const workModeFilters = getSelectedFilters('workMode');
    const experienceFilters = getSelectedFilters('experience');
    const salaryFilters = getSelectedFilters('salary');
    const departmentFilters = getSelectedFilters('department');
    const companyTypeFilters = getSelectedFilters('companyType');
    const roleCategoryFilters = getSelectedFilters('roleCategory');
    const locationFilters = getSelectedFilters('location');

    jobCards.forEach(card => {
        const workMode = card.querySelector('.job-details').textContent.toLowerCase();
        const location = card.querySelector('.job-details').textContent.toLowerCase();

        let show = true;

        if (workModeFilters.length && !workModeFilters.some(filter => workMode.includes(filter))) {
            show = false;
        }

        if (locationFilters.length && !locationFilters.some(filter => location.includes(filter))) {
            show = false;
        }

        if (show) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function getSelectedFilters(filterName) {
    const checkboxes = document.querySelectorAll(`input[name="${filterName}"]:checked`);
    return Array.from(checkboxes).map(checkbox => checkbox.value.toLowerCase());
}

document.querySelector('button').addEventListener('click', filterJobs);


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