document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const responseArea = document.getElementById('responseArea');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        responseArea.innerHTML = 'Processing...';

        fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.frames) {
                    displayFrames(data.frames);
                } else {
                    responseArea.innerHTML = 'Failed to process video.';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                responseArea.innerHTML = 'Error processing video.';
            });
    });

    function displayFrames(frames) {
        responseArea.innerHTML = '';
        frames.forEach(frame => {
            const img = document.createElement('img');
            img.src = frame;
            img.style.width = '100px'; // Adjust size as needed
            img.style.height = 'auto';
            img.style.margin = '5px';
            responseArea.appendChild(img);
        });
    }
});