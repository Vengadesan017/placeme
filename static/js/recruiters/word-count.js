const textarea = document.getElementById("count-words");
const charCountDisplay = document.getElementById("char-count");

// Use the maxlength attribute if set, otherwise default to 500
const maxLength = textarea.maxLength > 0 ? textarea.maxLength : 200;

textarea.addEventListener("input", function () {
    const text = textarea.value;
    const charCount = text.length;

    charCountDisplay.textContent = `${charCount}/${maxLength} characters`;

    if (charCount > maxLength) {
        charCountDisplay.style.color = "red";
    } else {
        charCountDisplay.style.color = "#555";
    }
});
