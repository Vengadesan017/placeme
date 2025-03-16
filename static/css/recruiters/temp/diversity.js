const openBox = document.getElementById('open-fa-caret-right');
const employementBody = document.getElementById('employement-body');

openBox.addEventListener('click', () => {
    const rRight = document.getElementById('r-right')
    if (employementBody.style.display === 'none' || employementBody.style.display === '') {
        employementBody.style.display = 'flex';
        // rRight.style.height = '1300px' 
    } else {
        employementBody.style.display = 'none';
    }
});



const openBoxEducation = document.getElementById('open-education');
const educationBody = document.getElementById('education-body');

openBoxEducation.addEventListener('click', () => {
    const rRight = document.getElementById('r-right')
    if (educationBody.style.display === 'none' || educationBody.style.display === '') {
        educationBody.style.display = 'flex'; 
        // rRight.style.height = '1500px' 
    } else {
        educationBody.style.display = 'none';
        
    }
});





const openBoxDiversity = document.getElementById('open-diversity');
const diversityBody = document.getElementById('diversity-body');

openBoxDiversity.addEventListener('click', () => {
    const rRight = document.getElementById('r-right')
    if (diversityBody.style.display === 'none' || diversityBody.style.display === '') {
        // rRight.style.height = '1800px'
        diversityBody.style.display = 'flex'; 
    } else {
        diversityBody.style.display = 'none';
        // rRight.style.height = '1500px'
    }
});



document.addEventListener("DOMContentLoaded", function () {
    const candidates = document.querySelectorAll(".select-candidate");

    candidates.forEach(candidate => {
        candidate.addEventListener("click", function () {
            // Toggle the "active" class (select/unselect)
            this.classList.toggle("active");
        });
    });
});
