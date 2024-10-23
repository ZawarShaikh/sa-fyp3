document.addEventListener("DOMContentLoaded", function () {
    // Data for Text Sentiment Chart
    var textPositive = parseInt(document.getElementById("text-positive-count").value);
    var textNegative = parseInt(document.getElementById("text-negative-count").value);
    var textNeutral = parseInt(document.getElementById("text-neutral-count").value);

    // Data for Audio Sentiment Chart
    var audioPositive = parseInt(document.getElementById("audio-positive-count").value);
    var audioNegative = parseInt(document.getElementById("audio-negative-count").value);
    var audioNeutral = parseInt(document.getElementById("audio-neutral-count").value);

    // Data for Video Sentiment Chart
    var videoPositive = parseInt(document.getElementById("video-positive-count").value);
    var videoNegative = parseInt(document.getElementById("video-negative-count").value);
    var videoNeutral = parseInt(document.getElementById("video-neutral-count").value);

    // Create the Text Pie Chart
    var textCtx = document.getElementById('textSentimentChart').getContext('2d');
    new Chart(textCtx, {
        type: 'pie',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                label: 'Text Sentiment',
                data: [textPositive, textNegative, textNeutral],
                backgroundColor: ['#4CAF50', '#F44336', '#FFC107']
            }]
        }
    });

    // Create the Audio Pie Chart
    var audioCtx = document.getElementById('audioSentimentChart').getContext('2d');
    new Chart(audioCtx, {
        type: 'pie',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                label: 'Audio Sentiment',
                data: [audioPositive, audioNegative, audioNeutral],
                backgroundColor: ['#4CAF50', '#F44336', '#FFC107']
            }]
        }
    });

    // Create the Video Pie Chart
    var videoCtx = document.getElementById('videoSentimentChart').getContext('2d');
    new Chart(videoCtx, {
        type: 'pie',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                label: 'Video Sentiment',
                data: [videoPositive, videoNegative, videoNeutral],
                backgroundColor: ['#4CAF50', '#F44336', '#FFC107']
            }]
        }
    });
});



function redirectProduct() {
    var selectedProduct = document.getElementById("productSelect").value;

    if (selectedProduct) {
        fetch("/fetch_product_data", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ product: selectedProduct })
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response (e.g., display the reviews in a table)
            displayProductReviews(data);
        })
        .catch(error => console.error('Error:', error));
    }
}

function displayProductReviews(reviews) {
    const tableBody = document.querySelector("#reviewsTable tbody");
    tableBody.innerHTML = ''; // Clear previous reviews

    reviews.forEach(review => {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.textContent = review[0];  // Assuming review is a tuple (review,)
        row.appendChild(cell);
        tableBody.appendChild(row);
    });
}
