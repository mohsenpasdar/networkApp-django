document.addEventListener('DOMContentLoaded', function () {

    // Select all SVG elements with an ID that starts with "heart-icon-"
    const svgs = document.querySelectorAll("[id^='heart-icon-']");
    // Loop through each SVG element
    svgs.forEach(svg => {
        // Add a click event listener to the parent element of the SVG
        svg.addEventListener('click', () => {
            // Change the fill color of the SVG to red when it is clicked
            svg.parentElement.classList.toggle('liked');
        });
    });
})
