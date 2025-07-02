let loadingTimeout = null;

function startLoading(event = null) {
    // Schedule the loader to appear after 350ms
    loadingTimeout = setTimeout(() => {
        document.getElementById('loading-screen').style.display = 'block';
    }, 350);
}

function stopLoading(event = null) {
    // Cancel the pending loader
    if (loadingTimeout !== null) {
        clearTimeout(loadingTimeout);
        loadingTimeout = null;
    }

    // Hide loader after a short delay to allow animations, if any
    setTimeout(() => {
        document.getElementById('loading-screen').style.display = 'none';
    }, 100);  // You can adjust this delay (or set to 0)
}


  // refresh page when htmx return full page
function checkIfFullPage(event) {
    const html = event.detail.xhr.responseText;
    if (html.includes("<!DOCTYPE html>")) {
        // Redirect to the actual page instead of rendering it inside
        window.location.href = event.detail.xhr.responseURL;
    }
}

// htmx.on("htmx:responseError", (e) => console.error("HTMX Response Error:", e.detail));
// htmx.on("htmx:sendError", (e) => console.error("HTMX Send Error:", e.detail));
