

document.querySelectorAll('.fa-ellipsis-vertical').forEach(menuBar => {
    menuBar.addEventListener('click', function(event) {
        // Find the closest parent box
        let parentBox = event.target.closest('.right-box-1'); // Adjust class if needed
        if (parentBox) {
            let c3Post = parentBox.querySelector('.c-3-postion'); // Get the corresponding menu inside the parent
            if (c3Post) {
                // Toggle display
                c3Post.style.display = (c3Post.style.display === "none" || c3Post.style.display === "") ? "flex" : "none";
            }
        }
    });
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

// const filterDiv = document.getElementById('m-filter-div'); // Filter button
// const xMark = document.querySelector('.x-mark'); // X close button

// filterDiv.addEventListener('click', function () {
//     mobileView(true); // Show filter when clicked
// });

// xMark.addEventListener('click', function () {
//     mobileView(false); // Hide filter when clicked
// });

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








