



const textarea = document.getElementById("book-description-input");
const charCountDisplay = document.getElementById("char-count");

textarea.addEventListener("input", function() {

    const text = textarea.value;
    
    const charCount = text.length;
    
    const maxLength = 500;

    charCountDisplay.textContent = `${charCount}/${maxLength} char`;
    
    if (charCount > maxLength) {
        charCountDisplay.style.color = "red";
    } else {
        charCountDisplay.style.color = "#555"; 
        
    }
});

function toggleDescription(element) {
    element.classList.toggle("expanded");
}