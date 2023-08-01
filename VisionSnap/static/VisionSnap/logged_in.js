// logged_in.js

// Set the maxHeight of the collapsible content to 0px when the page loads
window.onload = function() {
    document.getElementById("collapseContent").style.maxHeight = "0px";
}

// Function to toggle collapse
function toggleCollapse(collapseId) {
    const content = document.getElementById(collapseId);
    if (content.style.maxHeight) {
        content.style.maxHeight = null;
    } else {
        content.style.maxHeight = content.scrollHeight + "px";
    } 
}

document.addEventListener('DOMContentLoaded', (event) => {
    const imageInput = document.getElementById("imageInput");
    const allPred = document.getElementById("allPred");
    const selectedPred = document.getElementById("selectedPred");
        
    const allPredData = JSON.parse(document.getElementById('allPredData').textContent);
    
    const selectedPredData = JSON.parse(document.getElementById('selectedPredData').textContent);
    
    allPredData.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        allPred.appendChild(li);
    }); 
    
    selectedPredData.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        selectedPred.appendChild(li);
    });

    const loadUrlButton = document.getElementById("loadUrlButton");
    const imageUrlInput = document.getElementById("imageUrlInput");
    const imageDisplay = document.getElementById("imageDisplay");
    const placeholder = document.getElementById("placeholder");

    loadUrlButton.onclick = () => {
        const xhr = new XMLHttpRequest();
        const processUrl = JSON.parse(document.getElementById('process_url').textContent); // Use JSON.parse here
        xhr.open("POST", processUrl, true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.setRequestHeader("X-CSRFToken", document.getElementById('csrfToken').textContent);
    
        xhr.onreadystatechange = function() {
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                const res = JSON.parse(this.responseText);
                if (res.status === 'success') {
                    imageDisplay.src = 'data:image/jpeg;base64,' + res.image;
                    imageDisplay.style.display = "block";  
                    placeholder.style.display = "none"; 
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
    
    imageInput.onchange = (e) => {
        const reader = new FileReader();

        reader.onload = (event) => {
            imageDisplay.src = event.target.result;
            imageDisplay.style.display = "block";
            placeholder.style.display = "none";
        }
        reader.readAsDataURL(e.target.files[0]);
    }
});

// Global variable to keep track of checkbox selections
var predClassSelection = [];

function updatePredClassSelection(key) {
    const checkbox = document.getElementById(key);
    if (checkbox.checked) {
        if (!predClassSelection.includes(key)) {
            predClassSelection.push(key);
        }
    } else {
        const index = predClassSelection.indexOf(key);
        if (index > -1) {
            predClassSelection.splice(index, 1);
        }
    }

    // Now send the updated selection to the server
    sendPredClassSelection();
}

function sendPredClassSelection() {
    const xhr = new XMLHttpRequest();
    const updateUrl = '/update_pred_class_selection/'; // Specify the URL to send the data to
    xhr.open("POST", updateUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", document.getElementById('csrfToken').textContent);
    
    xhr.send(JSON.stringify(predClassSelection));
}