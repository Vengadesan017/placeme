document.addEventListener('DOMContentLoaded', function () {

    const multiSelectConfigs = [
        ['multi-select-qualifications', 'search-qualifications', 'selected-tags-qualifications', 'dropdown-qualifications', 'new-qualifications'],
        ['multi-select-location', 'search-location', 'selected-tags-location', 'dropdown-location', 'new-locations'],
        ['multi-select-skills', 'search-skills', 'selected-tags-skills', 'dropdown-skills', 'new-skills'],
        ['multi-select-benefits', 'search-benefits', 'selected-tags-benefits', 'dropdown-benefits', 'new-benefits']
    ];

    fetch('./../api/create-job-form/')
        .then(response => response.json())
        .then(data => {
            function appendOptions(dataList, selectId) {
                const select = document.getElementById(selectId);
                const existingValues = new Set(Array.from(select.options).map(opt => opt.value));
                const fragment = document.createDocumentFragment();

                dataList.forEach(item => {
                    if (!existingValues.has(item.id.toString())) {
                        const option = document.createElement('option');
                        option.value = item.id;
                        option.textContent = item.name;
                        fragment.appendChild(option);
                    }
                });

                select.appendChild(fragment);
            }

            appendOptions(data.locations, 'multi-select-location');
            appendOptions(data.skills, 'multi-select-skills');
            appendOptions(data.qualifications, 'multi-select-qualifications');
            appendOptions(data.benefits, 'multi-select-benefits');

            // Initialize multi-selects AFTER data is loaded
            multiSelectConfigs.forEach(config => setupMultiSelect(...config));
        })
        .catch(error => {
            console.error('Error loading dropdown data:', error);
        });

    function setupMultiSelect(selectId, searchInputId, tagsContainerId, dropdownId, newQualInputId) {
        const select = document.querySelector(`#${selectId}`);
        const searchInput = document.querySelector(`#${searchInputId}`);
        const tagsContainer = document.querySelector(`#${tagsContainerId}`);
        const dropdown = document.querySelector(`#${dropdownId}`);
        const newQualInput = document.querySelector(`#${newQualInputId}`);

        let selectedValues = [];
        let newItems = [];

        function getOptions() {
            return Array.from(select.options);
        }

        function renderDropdown(filteredOptions = getOptions()) {
            if (searchInput !== document.activeElement && searchInput.value.trim() === "") {
                dropdown.style.display = "none";
                return;
            }

            dropdown.innerHTML = '';
            const fragment = document.createDocumentFragment();

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
                    fragment.appendChild(item);
                }
            });

            dropdown.appendChild(fragment);
            dropdown.style.display = filteredOptions.length > 0 ? "block" : "none";
        }

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
            if (!selectedValues.includes(option.value)) {
                selectedValues.push(option.value);
                option.selected = true;
                addTag(option.text, false, option.value);
                renderDropdown();
            }
        }

        function selectNewOption(text) {
            if (!newItems.includes(text)) {
                newItems.push(text);
                updateNewInput();
                addTag(text, true);
            }
        }

        function updateNewInput() {
            newQualInput.value = newItems.join(',');
        }

        searchInput.addEventListener('focus', () => {
            const query = searchInput.value.toLowerCase();
            const filtered = getOptions().filter(opt => opt.text.toLowerCase().includes(query));
            renderDropdown(filtered);
        });

        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase();
            const filtered = getOptions().filter(opt => opt.text && opt.text.toLowerCase().includes(query));
            renderDropdown(filtered);
        });

        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const inputValue = searchInput.value.trim();
                if (inputValue === '') return;

                const existingOption = getOptions().find(opt => opt.text.toLowerCase() === inputValue.toLowerCase());
                if (existingOption) {
                    selectExistingOption(existingOption);
                } else {
                    selectNewOption(inputValue);
                }

                searchInput.value = '';
            }
        });

        // Add a global click-outside listener only once (optimized)
        document.addEventListener('click', function (e) {
            if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.style.display = "none";
            }
        });
    }
});
