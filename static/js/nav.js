document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.getElementById("menu-toggle");

    toggle.addEventListener("click", function () {
        // Toggle the active class on the menu items
        var items = document.querySelectorAll(".item");
        items.forEach(function (item) {
            item.classList.toggle("open");
        });

        // Toggle the active class on the menu icon
        this.classList.toggle("open");
    });
});