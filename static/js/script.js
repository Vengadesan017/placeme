document.addEventListener('DOMContentLoaded', function () {
    var mobileField = document.getElementById('mobileField');

    mobileField.addEventListener('input', function () {
        var validity = this.validity;

        // Check if the input value is valid according to the pattern
        if (!validity.valid) {
            this.setCustomValidity(validity.valid);
        } else {
            this.setCustomValidity('');
        }
    });
});


