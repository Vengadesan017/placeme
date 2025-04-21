  function handleFormSubmit(formId) {
    const form = document.getElementById(formId);
    let clickedButton = null;

    if (!form) return;

    // Track which submit button was clicked
    form.addEventListener('click', function (e) {
        if (e.target.type === 'submit') {
            clickedButton = e.target;
        }
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        startLoading();
        let check = true;
        const formData = new FormData(form);

        if (clickedButton && clickedButton.name) {
            formData.append(clickedButton.name, clickedButton.value);
        }

        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            form.reset();
            closeOpenedModal();

            // Optional: Refresh relevant data depending on form
            if (formId === 'create-new-position-id') {
                getPositions();
            } else if (formId === 'create-new-hire-request-id') {
                getPositions();
            }

            if (data.error) {
                displayApiMessages(data.error, 'error');
                check = false;
            }
            if (data.info) {
                displayApiMessages(data.info, 'info');
                check = false;
            }
            if (data.warning) {
                displayApiMessages(data.warning, 'warning');
                check = false;
            }
            if (check) {
                displayApiMessages('Something went wrong, Please wait or refresh.', 'warning');
              }
              check = true;
        })
        .catch(error => {
          form.reset();
          closeOpenedModal();
            if (error.error) {
                displayApiMessages(error.error, 'error');
                check = false;
            }
            if (error.info) {
                displayApiMessages(error.info, 'info');
                check = false;
            }
            if (error.warning) {
                displayApiMessages(error.warning, 'warning');
                check = false;
            }
            if (check) {
                displayApiMessages('Something went wrong, Please try again.', 'error');
              }
              check = true;
        })
        .finally(() => {
            stopLoading();
        });
    });
}
