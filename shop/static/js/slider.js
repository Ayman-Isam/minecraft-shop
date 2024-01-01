// Select all range input elements
const rangeInput = document.querySelectorAll('.range-input input');
let minValue = document.getElementById('min-value');
let maxValue = document.getElementById('max-value');
let progress = document.querySelector('.slider .progress');
let priceGap = 10;

// Add an input event listener to each range input
rangeInput.forEach(input => {
    input.addEventListener('input', e => {
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);

        // If the gap between the min and max values is less than the price gap
        if (maxVal - minVal < priceGap) {
            if(e.target.className === 'range-min') {
                rangeInput[0].value = maxVal - priceGap;
            } else {
                rangeInput[1].value = minVal + priceGap;
            }
        } else {
            // Update the min and max value text and the progress bar
            minValue.textContent = minVal;
            maxValue.textContent = maxVal;
            progress.style.left = (minVal / rangeInput[0].max) * 100 + '%';
            progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + '%';
        }
    });
});

// Trigger the input event for both range inputs when the page loads
window.onload = function() {
    setTimeout(function() {
        rangeInput[0].dispatchEvent(new Event('input'));
        rangeInput[1].dispatchEvent(new Event('input'));
    }, 100);
};