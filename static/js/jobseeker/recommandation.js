const searchInput = document.getElementById("searchInput");
const recommendationBox = document.getElementById("recommendationBox");
const recommendationItems = Array.from(recommendationBox.getElementsByClassName("recommendation-item"));

const locationInput = document.getElementById("locationInput");
const locationRecommendationBox = document.getElementById("locationRecommendationBox");
const locationItems = Array.from(locationRecommendationBox.getElementsByClassName("recommendation-item"));

const searchBar = document.querySelector(".search-bar");

document.addEventListener("click", (e) => {
    if (!searchInput.contains(e.target) && !recommendationBox.contains(e.target)) {
        recommendationBox.style.display = "none";
    }
    if (!locationInput.contains(e.target) && !locationRecommendationBox.contains(e.target)) {
        locationRecommendationBox.style.display = "none";
    }
});

searchInput.addEventListener("focus", () => {
    filterRecommendations(searchInput.value);
    showExtraInputsIfMobile();
});

searchInput.addEventListener("input", () => {
    filterRecommendations(searchInput.value);
    showExtraInputsIfMobile();
});

recommendationItems.forEach(item => {
    item.addEventListener("click", () => {
        searchInput.value = item.textContent.trim();
        recommendationBox.style.display = "none";
    });
});

function filterRecommendations(query) {
    const q = query.toLowerCase();
    const currentItems = Array.from(recommendationBox.getElementsByClassName("recommendation-item"));
    let visible = false;

    currentItems.forEach(item => {
        const match = item.textContent.toLowerCase().includes(q);
        item.style.display = match ? "block" : "none";
        if (match) visible = true;
    });

    recommendationBox.style.display = visible ? "block" : "none";
}

function filterLocations(query) {
    const q = query.toLowerCase();
    const currentItems = Array.from(locationRecommendationBox.getElementsByClassName("recommendation-item"));
    let visible = false;

    currentItems.forEach(item => {
        const match = item.textContent.toLowerCase().includes(q);
        item.style.display = match ? "block" : "none";
        if (match) visible = true;
    });

    locationRecommendationBox.style.display = visible ? "block" : "none";
}


locationInput.addEventListener("focus", () => {
    filterLocations(locationInput.value);
});

locationInput.addEventListener("input", () => {
    filterLocations(locationInput.value);
});

locationItems.forEach(item => {
    item.addEventListener("click", () => {
        locationInput.value = item.textContent.trim();
        locationRecommendationBox.style.display = "none";
    });
});

// function filterLocations(query) {
//     const q = query.toLowerCase();
//     let visible = false;
//     locationItems.forEach(item => {
//         const match = item.textContent.toLowerCase().includes(q);
//         item.style.display = match ? "block" : "none";
//         if (match) visible = true;
//     });
//     locationRecommendationBox.style.display = visible ? "block" : "none";
// }

function showExtraInputsIfMobile() {
    if (window.innerWidth <= 600) {
        searchBar.classList.add("show-extra");
    }
}