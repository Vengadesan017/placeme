document.addEventListener("DOMContentLoaded", function () {
    // Employment Section Toggle
    const openBox = document.getElementById("open-fa-caret-right");
    const employementBody = document.getElementById("employement-body");
    
    openBox.addEventListener("click", () => {
        if (employementBody.style.display === "none" || !employementBody.style.display) {
            employementBody.style.display = "flex";
        } else {
            employementBody.style.display = "none";
        }
    });

    // Education Section Toggle
    const openBoxEducation = document.getElementById("open-education");
    const educationBody = document.getElementById("education-body");
    
    openBoxEducation.addEventListener("click", () => {
        if (educationBody.style.display === "none" || !educationBody.style.display) {
            educationBody.style.display = "flex";
        } else {
            educationBody.style.display = "none";
        }
    });

    // Diversity Section Toggle
    const openBoxDiversity = document.getElementById("open-diversity");
    const diversityBody = document.getElementById("diversity-body");
    
    openBoxDiversity.addEventListener("click", () => {
        if (diversityBody.style.display === "none" || !diversityBody.style.display) {
            diversityBody.style.display = "flex";
        } else {
            diversityBody.style.display = "none";
        }
    });

    // Additional Section Toggle
    const openBoxAdditional = document.getElementById("open-additional");
    const additionalBody = document.getElementById("additional-body");
    
    openBoxAdditional.addEventListener("click", () => {
        if (additionalBody.style.display === "none" || !additionalBody.style.display) {
            additionalBody.style.display = "flex";
        } else {
            additionalBody.style.display = "none";
        }
    });

    // Candidate Selection Toggle
    const candidates = document.querySelectorAll(".select-candidate");
    
    candidates.forEach(candidate => {
        candidate.addEventListener("click", function () {
            this.classList.toggle("active");
        });
    });

    // Education Candidate Selection with Input Toggle
    const candidatesEdu = document.querySelectorAll(".select-candidate-edu");
    const classMap = {
        "10th": "tenth",
        "12th": "twelfth",
        "UG": "ug",
        "PG": "pg",
        "Diplomo": "diplomo",
        "PHD": "phd"
    };

    candidatesEdu.forEach(candidate => {
        candidate.addEventListener("click", function () {
            const selectedText = this.textContent.trim();
            const targetClass = classMap[selectedText];

            if (targetClass) {
                const targetDiv = document.querySelector(`.${targetClass}`);
                if (targetDiv) {
                    this.classList.toggle("active");
                    targetDiv.style.display = this.classList.contains("active") ? "flex" : "none";
                }
            }
        });
    });
})