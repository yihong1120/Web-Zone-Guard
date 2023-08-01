// logged_in.js

// When the document is loaded, this event listener will be triggered
document.addEventListener('DOMContentLoaded', (event) => {
    // Get necessary DOM elements
    const imageInput = document.getElementById("imageInput");
    const allPred = document.getElementById("allPred");
    const selectedPred = document.getElementById("selectedPred");

    // Get JSON data from hidden script tags
    const allPredData = JSON.parse(document.getElementById('allPredData').textContent);
    const selectedPredData = JSON.parse(document.getElementById('selectedPredData').textContent);

    // Append all predicates data to unordered list
    allPredData.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        allPred.appendChild(li);
    });

    // Append selected predicates data to unordered list
    selectedPredData.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        selectedPred.appendChild(li);
    });

    // Get necessary DOM elements for image loading
    const loadUrlButton = document.getElementById("loadUrlButton");
    const imageUrlInput = document.getElementById("imageUrlInput");
    const imageDisplay = document.getElementById("imageDisplay");
    const placeholder = document.getElementById("placeholder");

    // Add event listener for button click
    loadUrlButton.onclick = () => {
        const xhr = new XMLHttpRequest();
        const processUrl = JSON.parse(document.getElementById('process_url').textContent); // Use JSON.parse here
        xhr.open("POST", processUrl, true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.setRequestHeader("X-CSRFToken", document.getElementById('csrfToken').textContent);

        // Handle response
        xhr.onreadystatechange = function() {
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                const res = JSON.parse(this.responseText);
                // If image is successfully processed, display it
                if (res.status === 'success') {
                    imageDisplay.src = 'data:image/jpeg;base64,' + res.image;
                    imageDisplay.style.display = "block";
                    placeholder.style.display = "none";
                // If image is being streamed, update the display as the data comes in
                } else if (res.status === 'stream') {
                    let source = new EventSource(processUrl);
                    source.onmessage = function(event) {
                        imageDisplay.src = 'data:image/jpeg;base64,' + event.data;
                        imageDisplay.style.display = "block";
                        placeholder.style.display = "none";
                    }
                }
            }
        }
        console.log("url=" + encodeURIComponent(imageUrlInput.value));
        xhr.send("url=" + encodeURIComponent(imageUrlInput.value));
    }

    // Add event listener for image file input change
    imageInput.onchange = (e) => {
        const reader = new FileReader();

        reader.onload = (event) => {
            // Display the selected image
            imageDisplay.src = event.target.result;
            imageDisplay.style.display = "block";
            placeholder.style.display = "none";
        }
        reader.readAsDataURL(e.target.files[0]);
    }
});

// Global variable to keep track of checkbox selections
let predClassSelection = [];

// Update the prediction class selection when a checkbox is checked/unchecked
function updatePredClassSelection(key) {
    const checkbox = document.getElementById(key);
    // If checked, add to selection
    if (checkbox.checked) {
        if (!predClassSelection.includes(key)) {
            predClassSelection.push(key);
        }
    // If unchecked, remove from selection
    } else {
        const index = predClassSelection.indexOf(key);
        if (index > -1) {
            predClassSelection.splice(index, 1);
        }
    }

    // Now send the updated selection to the server
    sendPredClassSelection();
}

// Send the current prediction class selection to the server
function sendPredClassSelection() {
    const xhr = new XMLHttpRequest();
    const updateUrl = '/update_pred_class_selection/'; // Specify the URL to send the data to
    xhr.open("POST", updateUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", document.getElementById('csrfToken').textContent);

    xhr.send(JSON.stringify(predClassSelection));
}
