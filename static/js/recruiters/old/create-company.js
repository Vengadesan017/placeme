
const textarea = document.getElementById("book-description-input");
const charCountDisplay = document.getElementById("char-count");

textarea.addEventListener("input", function() {

    const text = textarea.value;
    
    const charCount = text.length;
    
    const maxLength = 200;

    charCountDisplay.textContent = `${charCount}/${maxLength} characters`;
    
    if (charCount > maxLength) {
        charCountDisplay.style.color = "red";
    } else {
        charCountDisplay.style.color = "#555"; 
        
    }
});

