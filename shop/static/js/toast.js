// Select the toast, close button, and progress bar elements
var toast = document.querySelector('.custom-toast');
var closeButton = document.querySelector('.close-button');
var progressBar = toast ? toast.querySelector('.toast-progress-bar') : null;

// Check if all elements exist
if (toast && closeButton && progressBar) {
  // When the close button is clicked, start the slideOut animation
  closeButton.addEventListener('click', function() {
    toast.classList.add('slideOut');
  });

  // Show the toast by starting the slideIn animation and setting display to block
  toast.classList.add('slideIn');
  toast.style.display = 'block';

  // Listen for the end of the slideIn animation
  toast.addEventListener('animationend', function(event) {
    if (event.animationName === 'slideIn') {
      progressBar.style.width = '100%';

      var timeLeft = 5000;
      var interval = setInterval(function() {
        if (!isPaused) {
          timeLeft -= 10;
          var newWidth = (timeLeft / 5000) * 100;
          progressBar.style.width = newWidth + '%';
        }

        if (timeLeft <= 0) {
          clearInterval(interval);
          toast.classList.add('slideOut');
        }
      }, 10); // Run every 10ms

      // Pause the countdown when the mouse is over the toast, and resume when it's not
      var isPaused = false;
      toast.addEventListener('mouseover', function() {
        isPaused = true;
      });
      toast.addEventListener('mouseout', function() {
        isPaused = false;
      });
    }
  });
}