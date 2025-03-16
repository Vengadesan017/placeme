
    // Get elements
    const searchInput = document.getElementById("searchInput");
    const recommendationBox = document.getElementById("recommendationBox");
    const recommendationItems = Array.from(recommendationBox.getElementsByClassName("recommendation-item"));

    // Show recommendations on focus
    searchInput.addEventListener("focus", () => {
        if (searchInput.value) {
            filterRecommendations(searchInput.value);
        }
        recommendationBox.style.display = "block";
    });

    // Hide recommendations when clicking outside the input or box
    document.addEventListener("click", (event) => {
        if (!searchInput.contains(event.target) && !recommendationBox.contains(event.target)) {
            recommendationBox.style.display = "none";
        }
    });

    // Filter recommendations based on input
    searchInput.addEventListener("input", () => {
        filterRecommendations(searchInput.value);
    });

    function filterRecommendations(query) {
        const lowerCaseQuery = query.toLowerCase();
        let hasVisibleItems = false;

        recommendationItems.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (text.includes(lowerCaseQuery)) {
                item.style.display = "flex"; // Show matching items
                hasVisibleItems = true;
            } else {
                item.style.display = "none"; // Hide non-matching items
            }
        });

        // Show or hide the recommendation box based on whether there are visible items
        recommendationBox.style.display = hasVisibleItems ? "block" : "none";
    }
    
    recommendationItems.forEach(item => {
        item.addEventListener("click", () => {
            searchInput.value = item.textContent.trim(); // Set input value to clicked item
            recommendationBox.style.display = "none"; // Hide recommendation box
        });
    });
