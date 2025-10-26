// Mode toggle
const modeSwitch = document.getElementById('modeSwitch');
if (modeSwitch) {
  modeSwitch.addEventListener('change', () => {
    document.body.classList.toggle('dark');
  });
}

// Upload & Predict
const predictBtn = document.getElementById('predictBtn');
if (predictBtn) {
  predictBtn.addEventListener('click', async () => {
    const fileInput = document.getElementById('imageUpload');
    const status = document.getElementById('status');
    const uploadedImage = document.getElementById('uploadedImage');

    if (!fileInput.files.length) {
      alert("Please upload an image first!");
      return;
    }

    const file = fileInput.files[0];

    // Show loading indicator
    status.textContent = "Uploading and predicting...";
    uploadedImage.style.display = "none";
    document.getElementById('class').textContent = "";
    document.getElementById('confidence').textContent = "";

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        status.textContent = "Prediction failed. Check server logs.";
        return;
      }

      const result = await res.json();

      // Show result
      status.textContent = "Image uploaded successfully!";
      uploadedImage.src = URL.createObjectURL(file);
      uploadedImage.style.display = "block";
      document.getElementById('class').textContent = `Class: ${result.class}`;
      document.getElementById('confidence').textContent = `Confidence: ${(result.confidence * 100).toFixed(2)}%`;

    } catch (error) {
      console.error(error);
      status.textContent = "Error uploading image.";
    }
  });
}
