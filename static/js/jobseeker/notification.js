const scroll = document.getElementById("scroll-bg");
const item = document.getElementById("notification");

let hideTimeout; // To store the timeout ID
// Function to show scroll-bg
const showScrollBg = () => {
    clearTimeout(hideTimeout); // Cancel any pending hide action
    scroll.style.display = "flex";
};

// Function to hide scroll-bg with a delay
const hideScrollBg = () => {
    hideTimeout = setTimeout(() => {
        scroll.style.display = "none";
    }, 500); // Wait for 2 seconds before hiding
};

// Add event listeners
item.addEventListener('mouseover', showScrollBg);
item.addEventListener('mouseout', hideScrollBg);
scroll.addEventListener('mouseover', showScrollBg); // Keep visible on hover
scroll.addEventListener('mouseout', hideScrollBg);  // Hide when leaving scroll-bg
