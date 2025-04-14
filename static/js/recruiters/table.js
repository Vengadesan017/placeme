let jobOpen = document.getElementById('job-open');
jobOpen.addEventListener('click' , () => {
    let showInfoDiv = document.getElementById('show-info-div')
    if(showInfoDiv.style.display === "flex" || showInfoDiv.style.display === ""){
        showInfoDiv.style.display = 'none';
    }else if(showInfoDiv.style.display === "none"){
        showInfoDiv.style.display = 'flex'
    }else{
        showInfoDiv.style.display = 'flex' 
    }
})




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