document.addEventListener("DOMContentLoaded", function () {
                    
    // Generic function to handle custom multi-select behavior for any field
    function setupMultiSelect(selectId, searchInputId, tagsContainerId, dropdownId, newQualInputId) {
        const select = document.querySelector(`#${selectId}`);
        const searchInput = document.querySelector(`#${searchInputId}`);
        const tagsContainer = document.querySelector(`#${tagsContainerId}`);
        const dropdown = document.querySelector(`#${dropdownId}`);
        const newQualInput = document.querySelector(`#${newQualInputId}`);

        const options = Array.from(select.options);
        let selectedValues = [];
        let newItems = [];

        function renderDropdown(filteredOptions = options) {
            if (searchInput !== document.activeElement && searchInput.value.trim() === "") {
                dropdown.style.display = "none";
                return;
            }
        
            dropdown.innerHTML = '';
            filteredOptions.forEach(option => {
                if (!selectedValues.includes(option.value)) {
                    const item = document.createElement('div');
                    item.className = 'dropdown-item';
                    item.textContent = option.text;
                    item.dataset.value = option.value;
                    item.addEventListener('click', () => {
                        selectExistingOption(option);
                        dropdown.style.display = "none";
                    });
                    dropdown.appendChild(item);
                }
            });
        
            dropdown.style.display = filteredOptions.length > 0 ? "block" : "none";
        }

        // Show dropdown when input is focused
        searchInput.addEventListener('focus', () => {
            const query = searchInput.value.toLowerCase();
            const filtered = options.filter(opt => opt.text.toLowerCase().includes(query));
            renderDropdown(filtered);
        });

        // // Hide dropdown on click outside
        // document.addEventListener('click', function (e) {
        //     if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
        //         dropdown.style.display = "none";
        //     }
        // }); 
        function addTag(text, isNew = false, value = null) {
            const tag = document.createElement('div');
            tag.className = 'tag';
            tag.textContent = text;

            const remove = document.createElement('span');
            remove.className = 'remove-tag';
            remove.textContent = '×';
            remove.addEventListener('click', () => {
                tag.remove();
                if (isNew) {
                    newItems = newItems.filter(val => val !== text);
                    updateNewInput();
                } else {
                    const opt = select.querySelector(`option[value="${value}"]`);
                    if (opt) opt.selected = false;
                    selectedValues = selectedValues.filter(val => val !== value);
                }
                renderDropdown();
            });

            tag.appendChild(remove);
            tagsContainer.appendChild(tag);
        }

        function selectExistingOption(option) {
            selectedValues.push(option.value);
            option.selected = true;
            addTag(option.text, false, option.value);
            renderDropdown();
        }

        function selectNewOption(text) {
            if (!newItems.includes(text)) {
                newItems.push(text);
                updateNewInput();
                addTag(text, true);
            }
        }

        function updateNewInput() {
            newQualInput.value = JSON.stringify(newItems); // Or comma-separated if you prefer
        }

        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase();
            const filtered = options.filter(opt => opt.text && opt.text.toLowerCase().includes(query));
            renderDropdown(filtered);
        });

        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const inputValue = searchInput.value.trim();
                if (inputValue === '') return;

                const existingOption = options.find(opt => opt.text.toLowerCase() === inputValue.toLowerCase());
                if (existingOption) {
                    selectExistingOption(existingOption);
                } else {
                    selectNewOption(inputValue);
                }

                searchInput.value = '';
            }
        });

        renderDropdown();
    }

    // Setup for qualifications
    setupMultiSelect('multi-select-qualifications', 'search-qualifications', 'selected-tags-qualifications', 'dropdown-qualifications', 'new-qualifications');
    
    // Setup for locations
    setupMultiSelect('multi-select-location', 'search-location', 'selected-tags-location', 'dropdown-location', 'new-locations');

    // Setup for Key Skills
    setupMultiSelect('multi-select-skills', 'search-skills', 'selected-tags-skills', 'dropdown-skills', 'new-skills');
    
    // Setup for benefits
    setupMultiSelect('multi-select-benefits', 'search-benefits', 'selected-tags-benefits', 'dropdown-benefits', 'new-benefits');
});