document.addEventListener("DOMContentLoaded", function () {
    // Get all the h2 elements inside the order_status class
    const statusElements = document.querySelectorAll(".order_status h2");
    
    // Loop through each element and apply color based on the status text
    statusElements.forEach(function (statusElement) {
        const status = statusElement.textContent.trim(); // Get the status text
        if (status === "Pending") {
            statusElement.style.color = "#DAA520"; // Apply yellow color for Pending
        } else if (status === "Cancelled") {
            statusElement.style.color = "red"; // Apply red color for Cancelled
        } else if (status === "Delivered") {
            statusElement.style.color = "green"; // Apply green color for Delivered
        }
    });
});


function scrollToCategoryByName(categoryName) {
    // Get all elements with id "item-title"
    const titles = document.querySelectorAll("#item-title");

    // Loop through the titles to find the matching category
    titles.forEach(title => {
        if (title.innerHTML.trim() === categoryName) {
            // Scroll to the matching category
            title.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    });
}
