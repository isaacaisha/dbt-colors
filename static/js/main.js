// Initialize a variable to store the selected color
let selectedColor = '';
// Function to convert RGB to hexadecimal format (#RRGGBB)
function rgbToHex(rgbColor) {
    const rgb = rgbColor.match(/\d+/g);
    return `#${parseInt(rgb[0]).toString(16).padStart(2, '0')}${parseInt(rgb[1]).toString(16).padStart(2, '0')}${parseInt(rgb[2]).toString(16).padStart(2, '0')};`;
}

// Function to display a "copied" message on the div
function displayCopiedMessage(element) {
    const messageElement = document.createElement('div');
    messageElement.textContent = 'Copied 👍🏿';
    messageElement.className = 'copied-message';
    element.appendChild(messageElement);
    // Remove the message element after a short delay (e.g., 2 seconds)
    setTimeout(() => {
        element.removeChild(messageElement);
    }, 1999); // 1.9 seconds
}

// Get all elements with the "color-box" class
const colorBoxes = document.querySelectorAll('.color-box');
// Add a click event listener to each color box
colorBoxes.forEach(box => {
    box.addEventListener('click', function() {
        // Get the background color of the clicked box
        const bgColor = window.getComputedStyle(this).getPropertyValue('background-color');
        // Convert the background color to hexadecimal format
        const hexColor = rgbToHex(bgColor);
        // Copy the hexadecimal color to the clipboard
        const dummyElement = document.createElement('textarea');
        dummyElement.value = hexColor;
        document.body.appendChild(dummyElement);
        dummyElement.select();
        document.execCommand('copy');
        document.body.removeChild(dummyElement);
        // Set the selectedColor variable to the hexadecimal color
        selectedColor = hexColor;
        // Display a "copied" message on the div
        displayCopiedMessage(this);
    });
});
