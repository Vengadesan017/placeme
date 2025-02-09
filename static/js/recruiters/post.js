let showMenuBar = document.getElementById('c-3-show');
let showMenuBar1 = document.getElementById('c-3-show-1');
let showMenuBar2 = document.getElementById('c-3-show-2');

// let PostDate = document.getElementById('Post-Date')

// PostDate.addEventListener('click' ,function(){
//     let PostDateClick = document.getElementById('post-date-click');
//     if(PostDateClick.style.display === 'none' || PostDateClick.style.display === ''){
//         PostDateClick.style.display = 'flex';
//     }else{
//         PostDateClick.style.display = 'none';
//     }
// })


showMenuBar.addEventListener('click', function() {
    let c3Post = document.getElementById('c-3-post');
    let c3Vacancy = document.getElementById('c-3-vacancy');
    // Check if display is 'none' or not set
    if (c3Post.style.display === "none" || c3Post.style.display === "") {
        c3Post.style.display = "flex";
        c3Vacancy.style.display = "flex";
    } else {
        c3Post.style.display = "none";
        c3Vacancy.style.display = "none";
    }
});

showMenuBar1.addEventListener('click', function() {
    let c3Post1 = document.getElementById('c-3-post-1');
    let c3Vacancy1 = document.getElementById('c-3-vacancy-1');
    // Check if display is 'none' or not set
    if (c3Post1.style.display === "none" || c3Post1.style.display === "") {
        c3Post1.style.display = "flex";
        c3Vacancy1.style.display = "flex";
    } else {
        c3Post1.style.display = "none";
        c3Vacancy1.style.display = "none";
    }
});

showMenuBar2.addEventListener('click', function() {
    let c3Post2 = document.getElementById('c-3-post-2');
    let c3Vacancy2 = document.getElementById('c-3-vacancy-2');
    // Check if display is 'none' or not set
    if (c3Post2.style.display === "none" || c3Post2.style.display === "") {
        c3Post2.style.display = "flex";
        c3Vacancy2.style.display = "flex";
    } else {
        c3Post2.style.display = "none";
        c3Vacancy2.style.display = "none";
    }
});

// const filterDiv = document.getElementById('m-filter-div');
// const xMark = document.getElementById('x-mark')
// filterDiv.addEventListener('click' , function(){
//     mobileView();
// })
// xMark.addEventListener('click' , function(){
//     mobileView();
// })

// const mobileView = () => {
    
    
//     if(window.innerWidth >= 320 && window.innerWidth <= 999){
//         let overLay = document.getElementById('overlay')
//         let m1ListDiv = document.getElementById("m1-filter-div")
//         if(overLay.style.display == 'none' || m1ListDiv.style.display == 'none' ){
//             overLay.style.display = 'flex';
//             m1ListDiv.style.display = 'flex';
//         }
//         if(overLay.style.display == 'flex' || m1ListDiv.style.display == 'flex'){
//             overLay.style.display = 'none';
//             m1ListDiv.style.display = 'none';
//         }

        
//     }

// }



// window.addEventListener('resize' , mobileView)

const filterDiv = document.getElementById('m-filter-div'); // Filter button
const xMark = document.querySelector('.x-mark'); // X close button

filterDiv.addEventListener('click', function () {
    mobileView(true); // Show filter when clicked
});

xMark.addEventListener('click', function () {
    mobileView(false); // Hide filter when clicked
});

const mobileView = (show) => {
    if (window.innerWidth >= 320 && window.innerWidth <= 999) {
        let overLay = document.getElementById('overlay');
        let m1ListDiv = document.getElementById("m1-filter-div");

        if (show) {
            overLay.style.display = 'flex';
            m1ListDiv.style.display = 'flex';
        } else {
            overLay.style.display = 'none';
            m1ListDiv.style.display = 'none';
        }
    }
};

// Hide when clicking on overlay
document.getElementById('overlay').addEventListener('click', function () {
    mobileView(false);
});

// Ensure mobile view updates on window resize
window.addEventListener('resize', function () {
    if (window.innerWidth > 999) {
        mobileView(false); // Hide the filter when switching to a larger screen
    }
});

