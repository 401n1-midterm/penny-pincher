const numberOfIterations = 5;
const delay = 30000;
let counter = delay / 1000;

// Check if results are ready
for (let i = 1; i < numberOfIterations + 1; i++) {
  setTimeout(() => {
    $.get(check_results_url, (data) => {
      let ready = data["ready"];
      let hasError = data["has_errors"];
      let errorMessage = data["error_message"];
      console.log(ready, hasError, errorMessage);

      // If results are ready - redirect to the results page
      if (ready || i === numberOfIterations || hasError) {
        window.location = results_url;
      }
      counter = delay / 1000;
    });
  }, delay * i);
}

// Handle the timer
$(() => {
  setInterval(() => {
    counter--;
    if (counter >= 0) {
      $("#count").text(counter);
    }
    if (counter === 0) {
      clearInterval(counter);
    }
  }, 1000);
});
