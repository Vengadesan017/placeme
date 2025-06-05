document.addEventListener('DOMContentLoaded', function () {
    // Fetch recommended job titles and locations
    fetch('./../api/keyword/')
        .then(response => response.json())
        .then(data => {
        populateRecommendations(data.titles, 'recommendationBox', document.getElementById('searchInput'));
        populateRecommendations(data.locations, 'locationRecommendationBox', document.getElementById('locationInput'));
        })
        .catch(error => {
            console.error('Error loading recommendations:', error);
        });

    // Populate a given recommendation box with items

function populateRecommendations(items, containerId, inputElement) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    items.forEach(item => {
        const text = typeof item === 'string' ? item : item.title || item.name || '';
        const div = document.createElement('div');
        div.className = 'recommendation-item';
        div.textContent = text;

        div.addEventListener('click', () => {
            const cleanText = text.split('(')[0].trim(); // Get only "Virumandampalayam"
            inputElement.value = cleanText;
            container.style.display = 'none';
        });
        container.appendChild(div);
    });

    // Rebind filtering and click logic (only for searchInput)
    if (inputElement.id === 'searchInput') {
        searchInput.addEventListener("input", () => {
            filterRecommendations(searchInput.value);
            showExtraInputsIfMobile();
        });

        searchInput.addEventListener("focus", () => {
            filterRecommendations(searchInput.value);
            showExtraInputsIfMobile();
        });
    }
}

});