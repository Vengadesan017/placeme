const scroll = document.getElementById("scroll-bg");
const item = document.getElementById("notification");

let hideTimeout;      // To store the timeout ID for hiding
let showTimeout;      // To store the timeout ID for showing

// Function to show scroll-bg with a delay
const showScrollBg = () => {
    clearTimeout(hideTimeout); // Cancel any pending hide
    clearTimeout(showTimeout); // Prevent multiple timers

    showTimeout = setTimeout(() => {
        scroll.style.display = "flex";
    }, 400); // Delay before showing (300ms)
};

// Function to hide scroll-bg with a delay
const hideScrollBg = () => {
    clearTimeout(showTimeout); // Cancel any pending show

    hideTimeout = setTimeout(() => {
        scroll.style.display = "none";
    }, 500); // Delay before hiding (300ms)
};

// Add event listeners
item.addEventListener("mouseenter", showScrollBg);
item.addEventListener("mouseleave", hideScrollBg);
scroll.addEventListener("mouseenter", showScrollBg);
scroll.addEventListener("mouseleave", hideScrollBg);
