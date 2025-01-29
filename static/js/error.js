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