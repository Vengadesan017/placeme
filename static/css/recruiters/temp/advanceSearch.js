document.addEventListener("DOMContentLoaded", function () {
    const skillInput = document.getElementById("skill-input");
    const skillContainer = document.getElementById("selected-skills");
    const suggestionBox = document.getElementById("suggestion-box");

    let suggestedSkills = ["JavaScript", "React", "Node.js", "CSS", "HTML", "Python", "Java", "C++", "TypeScript", "SQL"];
    let selectedSkills = [];

    skillInput.addEventListener("keyup", function (event) {
        let inputVal = skillInput.value.trim();
        let lastTypedSkill = inputVal.split(",").pop().trim(); // Get last typed skill

        if (event.key === "," || event.key === "Enter") {
            event.preventDefault();
            let skills = inputVal.split(",").map(s => s.trim()).filter(s => s);
            skills.forEach(skill => addSkill(skill));
            skillInput.value = selectedSkills.join(", ") + ", ";
            showSuggestions(""); // Reset suggestions
        } else if (event.key === "Tab" && suggestionBox.firstChild) {
            event.preventDefault();
            addSkill(suggestionBox.firstChild.textContent);
            skillInput.value = selectedSkills.join(", ") + ", ";
            showSuggestions(""); // Reset suggestions
        } else if (event.key === "Backspace" && skillInput.value.endsWith(", ")) {
            removeLastSkill();
        } else {
            showSuggestions(lastTypedSkill);
        }
    });

    function addSkill(skill) {
        skill = skill.charAt(0).toUpperCase() + skill.slice(1).toLowerCase(); // Capitalize first letter
        if (!selectedSkills.includes(skill) && skill !== "") {
            selectedSkills.push(skill);

            let skillBox = document.createElement("div");
            skillBox.classList.add("skill-box");

            let skillCheckbox = document.createElement("input");
            skillCheckbox.type = "checkbox";
            skillCheckbox.title = "Mark as mandatory";

            let skillText = document.createElement("p");
            skillText.textContent = skill;

            let removeButton = document.createElement("button");
            removeButton.textContent = "X";
            removeButton.classList.add("remove-skill");
            removeButton.onclick = function () {
                skillBox.remove();
                selectedSkills = selectedSkills.filter(s => s !== skill);
                updateInputText();
            };

            skillBox.appendChild(skillCheckbox);
            skillBox.appendChild(skillText);
            skillBox.appendChild(removeButton);
            skillContainer.appendChild(skillBox);

            updateInputText();
        }
    }

    function updateInputText() {
        skillInput.value = selectedSkills.join(", ") + ", ";
        showSuggestions(""); // Reset suggestions
    }

    function removeLastSkill() {
        if (selectedSkills.length > 0) {
            selectedSkills.pop();
            updateInputText();
        }
    }

    function showSuggestions(input) {
        if (!input) {
            suggestionBox.innerHTML = "";
            suggestionBox.style.display = "none";
            return;
        }

        let lowerCaseInput = input.toLowerCase();
        let filteredSuggestions = suggestedSkills.filter(skill =>
            skill.toLowerCase().startsWith(lowerCaseInput) && !selectedSkills.includes(skill)
        );

        suggestionBox.innerHTML = "";
        if (filteredSuggestions.length > 0) {
            filteredSuggestions.forEach(skill => {
                let suggestionItem = document.createElement("div");
                suggestionItem.classList.add("suggestion-item");
                suggestionItem.textContent = skill;
                suggestionItem.onclick = function () {
                    addSkill(skill);
                    skillInput.value = selectedSkills.join(", ") + ", ";
                    showSuggestions("");
                };
                suggestionBox.appendChild(suggestionItem);
            });
            suggestionBox.style.display = "block";
        } else {
            suggestionBox.style.display = "none";
        }
    }

    document.addEventListener("click", function (event) {
        if (!event.target.closest(".search-container")) {
            suggestionBox.style.display = "none";
        }
    });
});












document.addEventListener("DOMContentLoaded", function () {
    const skillInput = document.getElementById("language-input");
    const skillContainer = document.getElementById("selected-language");
    const suggestionBox = document.getElementById("suggestion-language");

    let suggestedSkills = ["English" , "Tamil" , "Hindi" , "Franch" , "Japanies" , "Bengali" , "Marathi" , "Telugu" , "Gujarati" , "Urdu"];
    let selectedSkills = [];

    skillInput.addEventListener("keyup", function (event) {
        let inputVal = skillInput.value.trim();
        let lastTypedSkill = inputVal.split(",").pop().trim(); // Get last typed skill

        if (event.key === "," || event.key === "Enter") {
            event.preventDefault();
            let skills = inputVal.split(",").map(s => s.trim()).filter(s => s);
            skills.forEach(skill => addSkill(skill));
            skillInput.value = selectedSkills.join(", ") + ", ";
            showSuggestions(""); // Reset suggestions
        } else if (event.key === "Tab" && suggestionBox.firstChild) {
            event.preventDefault();
            addSkill(suggestionBox.firstChild.textContent);
            skillInput.value = selectedSkills.join(", ") + ", ";
            showSuggestions(""); // Reset suggestions
        } else if (event.key === "Backspace" && skillInput.value.endsWith(", ")) {
            removeLastSkill();
        } else {
            showSuggestions(lastTypedSkill);
        }
    });

    function addSkill(skill) {
        skill = skill.charAt(0).toUpperCase() + skill.slice(1).toLowerCase(); // Capitalize first letter
        if (!selectedSkills.includes(skill) && skill !== "") {
            selectedSkills.push(skill);

            let skillBox = document.createElement("div");
            skillBox.classList.add("skill-box");

            let skillCheckbox = document.createElement("input");
            skillCheckbox.type = "checkbox";
            skillCheckbox.title = "Mark as mandatory";


            let skillText = document.createElement("p");
            skillText.textContent = skill;

            let removeButton = document.createElement("button");
            removeButton.textContent = "X";
            removeButton.classList.add("remove-skill");
            removeButton.onclick = function () {
                skillBox.remove();
                selectedSkills = selectedSkills.filter(s => s !== skill);
                updateInputText();
            };

            skillBox.appendChild(skillCheckbox);
            skillBox.appendChild(skillText);
            skillBox.appendChild(removeButton);
            skillContainer.appendChild(skillBox);

            updateInputText();
        }
    }

    function updateInputText() {
        skillInput.value = selectedSkills.join(", ") + ", ";
        showSuggestions(""); // Reset suggestions
    }

    function removeLastSkill() {
        if (selectedSkills.length > 0) {
            selectedSkills.pop();
            updateInputText();
        }
    }

    function showSuggestions(input) {
        if (!input) {
            suggestionBox.innerHTML = "";
            suggestionBox.style.display = "none";
            return;
        }

        let lowerCaseInput = input.toLowerCase();
        let filteredSuggestions = suggestedSkills.filter(skill =>
            skill.toLowerCase().startsWith(lowerCaseInput) && !selectedSkills.includes(skill)
        );

        suggestionBox.innerHTML = "";
        if (filteredSuggestions.length > 0) {
            filteredSuggestions.forEach(skill => {
                let suggestionItem = document.createElement("div");
                suggestionItem.classList.add("suggestion-item");
                suggestionItem.textContent = skill;
                suggestionItem.onclick = function () {
                    addSkill(skill);
                    skillInput.value = selectedSkills.join(", ") + ", ";
                    showSuggestions("");
                };
                suggestionBox.appendChild(suggestionItem);
            });
            suggestionBox.style.display = "block";
        } else {
            suggestionBox.style.display = "none";
        }
    }

    document.addEventListener("click", function (event) {
        if (!event.target.closest(".search-container")) {
            suggestionBox.style.display = "none";
        }
    });
});