// close button
document.addEventListener('DOMContentLoaded', () => {
    const closeButtons = document.querySelectorAll('.closebtn');

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const alert = button.parentElement;
            console.log(alert);
            alert.classList.add('alert-hide');
            setTimeout(() => { alert.style.display = 'none'; }, 600);
            console.log(alert);
        });
    });
});


// add error when api is used 
function displayApiMessages(messages, level = 'error') {
    const container = document.getElementById('api-message');
    container.innerHTML = ''; // Clear previous messages

    // Match Django's alert style
    container.className = `alert alert-${level}`;

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


function displayHtmxMessages(messages) {
    const container = document.getElementById('alert-container');
    container.innerHTML = ''; // Clear previous alerts

    // Helper to create one alert
    function createAlert(messageText, level = 'error') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${level}`;

        const closeBtn = document.createElement('span');
        closeBtn.className = 'closebtn';
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cursor = 'pointer';
        closeBtn.onclick = function () {
            alert.classList.add('alert-hide');
            setTimeout(() => {
                alert.remove();
            }, 600);
        };

        alert.appendChild(closeBtn);

        const messageNode = document.createElement('p');
        messageNode.textContent = messageText;

        alert.appendChild(messageNode);
        container.appendChild(alert);
    }

    // Handle object format
    if (typeof messages === 'object' && !Array.isArray(messages)) {
        for (const [field, value] of Object.entries(messages)) {
            const fieldMessages = Array.isArray(value.messages)
                ? value.messages
                : (typeof value.messages === 'string'
                    ? [value.messages]
                    : [String(value)]);  // fallback

            const level = value.level || 'error';

            fieldMessages.forEach(msg => {
                createAlert(`${field}: ${msg}`, level);
            });
        }
    } else {
        // Handle plain message (string or array fallback)
        const msg = typeof messages === 'string' ? messages : JSON.stringify(messages);
        createAlert(msg, 'error');
    }
}
