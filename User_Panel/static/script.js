// Text Script
var formsSection = document.getElementById('forms-section');
formsSection.style.display = 'none'


// Get all image elements and add event listener
var images = document.querySelectorAll('.analysis-image');
const pidTextInput = document.getElementById('pid-text');
const pidAudioInput = document.getElementById('pid-audio');
const pidVideoInput = document.getElementById('pid-video');

// Add event listener to each image
images.forEach((image) => {
    image.addEventListener('click', (event) => {
        const clickedImageId = event.target.getAttribute('id');
        
      
        alert(clickedImageId)
        
    
        showForms(event);

        pidTextInput.value = clickedImageId; // Set the pid for the text review
        console.log(pidTextInput.value)
        pidAudioInput.value = clickedImageId; // Set the pid for the audio review
        pidVideoInput.value = clickedImageId; // Set the pid for the video review
    });
});


// Function to show forms when click event occurs 
function showForms(event) {
    formsSection.style.display = 'block';
}
/*
images.forEach((image) => {
    image.addEventListener('click', (event) => {
      showForms(event);
    });
  });

// Attach event listeners to each image
images.forEach(function(image) {
    image.addEventListener('click', showForms);
});
*/






// Audio script
let mediaRecorder;
let audioChunks = [];
const recordButton = document.getElementById('record-audio');
const stopButton = document.getElementById('stop-audio');
const audioPlayback = document.getElementById('audio-playback');
const recordedAudioInput = document.getElementById('recorded-audio');

recordButton.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPlayback.src = audioUrl;

            // Convert to base64 and set to hidden input
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = function() {
                recordedAudioInput.value = reader.result;
            };
        };

        recordButton.disabled = true;
        stopButton.disabled = false;
    });
});

stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    recordButton.disabled = false;
    stopButton.disabled = true;

    console.log(recordedAudioInput.value);  // Print Base64 string for verification
});
  
