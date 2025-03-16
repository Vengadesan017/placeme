let openMenu = document.getElementById('open-menu');
let closeMenu = document.getElementById('close-menu');
let Box1 = document.querySelectorAll('.box-1 a');  
let BoxHide = document.querySelectorAll('.box-1-hide a');
let rLeft = document.querySelector('.r-left');
let rRight = document.querySelector('.r-right');
let Menu = document.querySelector('.menu');
let navBar = document.querySelector('.navbar');
let mobileMenuOpen = document.getElementById('mobile-menu-open');
let mobileMenuClose = document.getElementById('mobile-menu-close');
let mobileMenuBox = document.getElementById('mobile-menu-box');
let rRightDown = document.querySelector('.r-right-down');
// Ensure rRight has position set to relative or absolute


function updateMenuLayout() {
    if(window.innerWidth <= 320) {
        // Set the styles for smaller screens (320px or less)
        rRight.style.transition = "left 0.3s ease";
        // rLeft.style.width = '320px';
        rLeft.style.width = '100%';
        rLeft.style.zIndex = '3'; 
        Menu.style.zIndex = '1';  
        // Menu.style.width = '220px';
        // rRight.style.left = '100px';
    }else if(window.innerWidth >= 321 && window.innerWidth <= 375){
        rRight.style.transition = "left 0.3s ease";
        
            // rLeft.style.width = '375px';
            rLeft.style.width = '100%';
        
        rLeft.style.zIndex = '3'; 
        Menu.style.zIndex = '1'; 
    }else if(window.innerWidth >= 375 && window.innerWidth <= 425){
        rRight.style.transition = "left 0.3s ease";
        // rLeft.style.width = '425px';
        rLeft.style.width = '100%';
        rLeft.style.zIndex = '3'; 
        Menu.style.zIndex = '1'; 
    }else if(window.innerWidth >= 425 && window.innerWidth <= 775){
        rRight.style.transition = "left 0.3s ease";
        // rLeft.style.width = '768px';
        rLeft.style.width = '100%';
        rLeft.style.zIndex = '3'; 
        Menu.style.zIndex = '1'; 
    }else if(window.innerWidth >= 769 && window.innerWidth <= 1340){
        rLeft.style.width = '200px';  
        rRight.style.width = 'calc(100% - 200px)'
        rRight.style.marginLeft = '200px';
        // navBar.style.transition = "left 0.3s ease";
        navBar.style.width = 'calc(100% - 200px)' 
        // rRight.style.transition = "left 0.3s ease";
    }
    else if(window.innerWidth >= 1367){
        
        rLeft.style.width = '200px';  
        rRight.style.width = 'calc(100% - 200px)'
        rRight.style.marginLeft = '200px';
        // navBar.style.transition = "left 0.3s ease";
        navBar.style.width = 'calc(100% - 200px)' 
        // rRight.style.transition = "left 0.3s ease";
    }  
    else {
        // Set the styles for larger screens
        rRight.style.transition = "left 0.3s ease";
        rLeft.style.width = '200px';  
        rRight.style.width = 'calc(100% - 200px)'
        rRight.style.marginLeft = '200px';
        navBar.style.width = 'calc(100% - 200px)'
    }
}
function updateMenuLayoutClose() {
    if(window.innerWidth <= 320) {
        rLeft.style.width = '60px';
        // Menu.style.width = '260px';
        rRight.style.marginLeft = '60px';
    }else if(window.innerWidth >= 321 && window.innerWidth <= 375){
        rLeft.style.width = '60px';
        // Menu.style.width = '260px';
        rRight.style.marginLeft = '60px';
    }else if(window.innerWidth >= 375 && window.innerWidth <= 425){
        rLeft.style.width = '60px';
        // Menu.style.width = '260px';
        rRight.style.marginLeft = '60px';
    }else if(window.innerWidth >= 425 && window.innerWidth <= 775){
        rLeft.style.width = '60px';
        // Menu.style.width = '260px';
        rRight.style.marginLeft = '60px';
    }else if(window.innerWidth >= 1367){
        rLeft.style.width = '80px';  
        rRight.style.width = 'calc(100% - 80px)'
        rRight.style.marginLeft = '80px';
        navBar.style.width = 'calc(100% - 80px)'
    }else if(window.innerWidth >= 769 && window.innerWidth <= 1340){
        rLeft.style.width = '80px';  
        rRight.style.width = 'calc(100% - 80px)'
        rRight.style.marginLeft = '80px';
        navBar.style.width = 'calc(100% - 80px)'
    }
     else {
        rLeft.style.width = '80px';  
        rRight.style.width = 'calc(100% - 80px)'
        rRight.style.marginLeft = '80px';
        navBar.style.width = 'calc(100% - 80px)'
    }
}

// Handle open menu click event
openMenu.addEventListener('click', function() {
    openMenu.style.display = 'none';
    closeMenu.style.display = 'flex';
    
    Box1.forEach(item => item.style.display = 'flex');
    BoxHide.forEach(item => item.style.display = 'none');
    

    // rRight.style.position = 'relative';
    updateMenuLayout(); 
    //  // Update layout based on screen width
    
});

// Handle close menu click event
closeMenu.addEventListener('click', function() {
    openMenu.style.display = 'flex';
    closeMenu.style.display = 'none';
    
    Box1.forEach(item => item.style.display = 'none');
    BoxHide.forEach(item => item.style.display = 'flex');
    
    // rRight.style.position = 'relative';

    updateMenuLayoutClose();
});

// Handle mobile menu open event
mobileMenuOpen.addEventListener('click', function() {
    mobileMenuOpen.style.display = 'none';
    mobileMenuClose.style.display = 'flex';
    mobileMenuBox.style.display = 'flex';
});

// Handle mobile menu close event
mobileMenuClose.addEventListener('click', function() {
    mobileMenuOpen.style.display = 'flex';
    mobileMenuClose.style.display = 'none';
    mobileMenuBox.style.display = 'none';
});

// Optional: To update layout if the window is resized
window.addEventListener('resize', updateMenuLayout);
window.addEventListener('resize', updateMenuLayoutClose);