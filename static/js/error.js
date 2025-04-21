// close button
document.addEventListener('DOMContentLoaded', () => {
    const closeButtons = document.querySelectorAll('.closebtn');

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const alert = button.parentElement;
            alert.style.opacity = '0';
            setTimeout(() => { alert.style.display = 'none'; }, 600);
        });
    });
});


// add error when api is used 
function displayApiMessages(messages, level = 'error') {
    const container = document.getElementById('api-message');
    container.innerHTML = ''; // Clear previous messages

    // Match Django's alert style
    container.className = `alert alert-${level}`;
    container.style.position = 'relative';
    container.style.top = '70px';
    container.style.display = 'block';

    // Create close button
    const closeBtn = document.createElement('span');
    closeBtn.className = 'closebtn';
    closeBtn.innerHTML = '&times;';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.float = 'right';
    closeBtn.onclick = function () {
        container.style.display = 'none';
    };
    container.appendChild(closeBtn);

    // Message rendering logic
    if (typeof messages === 'object' && !Array.isArray(messages)) {
        for (const [field, errors] of Object.entries(messages)) {
            errors.forEach(error => {
                const p = document.createElement('p');
                p.textContent = `${field}: ${error}`;
                container.appendChild(p);
            });
        }
    } else if (Array.isArray(messages)) {
        messages.forEach(msg => {
            const p = document.createElement('p');
            p.textContent = msg;
            container.appendChild(p);
        });
    } else {
        const p = document.createElement('p');
        p.textContent = messages;
        container.appendChild(p);
    }
    // // Auto-hide after 7 seconds (optional)
    // setTimeout(() => {
    //     container.style.display = 'none';
    // }, 7000);
}