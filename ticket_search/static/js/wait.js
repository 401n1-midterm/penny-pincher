const numberOfIterations = 8;
const delay = 30000;
let counter = delay / 1000;

// Check if results are ready
for (let i = 1; i < numberOfIterations; i++) {
  setTimeout(() => {
    $.get(check_results_url, (data) => {
      let ready = data["ready"];
      console.log(ready);

      // If results are ready - redirect to the results page
      if (ready) {
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
