document.addEventListener("DOMContentLoaded", function () {

    const skillMore = document.getElementById('skill-more')
    const skillClose = document.getElementById('skill-close')
    const keyUl = document.getElementById('keyUl')


    skillMore.addEventListener('click', () => {
        keyUl.style.height = "auto"
        skillMore.style.display = "none"
        skillClose.style.display = "inline-block"
    })

    skillClose.addEventListener('click', () => {
        keyUl.style.height = "50px"
        skillMore.style.display = "inline-block"
        skillClose.style.display = "none"
    })




    const PreferredTextDiv = document.getElementById('PreferredTextDiv')
    const PreferredMoreBtn = document.getElementById('PreferredMoreBtn')
    const PreferredCloseBtn = document.getElementById('PreferredCloseBtn')

    PreferredMoreBtn.addEventListener('click', () => {
        PreferredTextDiv.style.height = 'auto';
        PreferredMoreBtn.style.display = 'none';
        PreferredCloseBtn.style.display = 'inline-block';
    })
    PreferredCloseBtn.addEventListener('click', () => {
        PreferredTextDiv.style.height = '50px';
        PreferredCloseBtn.style.display = 'none';
        PreferredMoreBtn.style.display = 'inline-block';
    })

    function wrapEmailText() {
        const email = document.getElementById('email')
        const emailText = email.textContent





        if (emailText.length > 23) {
            const wrappedText = emailText.match(/.{1,23}/g).join('<br>');
            email.innerHTML = wrappedText;
        }
    }
    wrapEmailText()




    const summaryParas = document.querySelectorAll(".summary-data-container1 p");

    summaryParas.forEach((summaryPara) => {
        let expanded = false;

        summaryPara.addEventListener("click", function () {
            if (!expanded) {
                summaryPara.style.display = "block";
                summaryPara.style.overflow = "visible";
                summaryPara.style.textOverflow = "unset";
                summaryPara.style.webkitLineClamp = "unset";
                summaryPara.style.webkitBoxOrient = "unset";
                summaryPara.style.height = "auto";
            } else {
                summaryPara.style.display = "-webkit-box";
                summaryPara.style.overflow = "hidden";
                summaryPara.style.textOverflow = "ellipsis";
                summaryPara.style.webkitLineClamp = "4";
                summaryPara.style.webkitBoxOrient = "vertical";
                summaryPara.style.height = "90px";
            }
            expanded = !expanded;
        });
    });
});








