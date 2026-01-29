function submitDiabetesForm() {
    const form = document.getElementById('diabetesForm');
    const formData = new FormData(form);
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('resultContainer');
    const submitBtn = document.getElementById('submitBtn');

    loading.style.display = 'block';
    resultContainer.style.display = 'none';
    submitBtn.disabled = true;

    fetch('/predict/diabetes', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = 'none';
        submitBtn.disabled = false;

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        displayResults(data);
    })
    .catch(error => {
        loading.style.display = 'none';
        submitBtn.disabled = false;
        alert('Error: ' + error);
    });
}

function submitHeartForm() {
    const form = document.getElementById('heartForm');
    const formData = new FormData(form);
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('resultContainer');
    const submitBtn = document.getElementById('submitBtn');

    loading.style.display = 'block';
    resultContainer.style.display = 'none';
    submitBtn.disabled = true;

    fetch('/predict/heart', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = 'none';
        submitBtn.disabled = false;

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        displayResults(data);
    })
    .catch(error => {
        loading.style.display = 'none';
        submitBtn.disabled = false;
        alert('Error: ' + error);
    });
}

function displayResults(data) {
    const resultContainer = document.getElementById('resultContainer');
    const predictionClass = data.prediction === 'Positive' || data.prediction.includes('Disease') ? 'positive' : 'negative';

    resultContainer.innerHTML = `
        <div class="result-item ${predictionClass}">
            <h3>Final Prediction</h3>
            <p><strong>Disease:</strong> ${data.disease}</p>
            <p><strong>Result:</strong> ${data.prediction}</p>
            <p><strong>Confidence:</strong> ${data.confidence}%</p>
            <p><strong>Risk Level:</strong> ${data.risk_level}</p>
        </div>

        <div class="result-item">
            <h3>Tabular Data Analysis</h3>
            <p><strong>Prediction:</strong> ${data.tabular_result.prediction}</p>
            <p><strong>Confidence:</strong> ${data.tabular_result.confidence.toFixed(2)}%</p>
            <p><strong>Risk Level:</strong> ${data.tabular_result.risk_level}</p>
        </div>

        <div class="result-item">
            <h3>Image Analysis</h3>
            <p><strong>Prediction:</strong> ${data.image_result.prediction}</p>
            <p><strong>Confidence:</strong> ${data.image_result.confidence.toFixed(2)}%</p>
            <p><strong>Risk Level:</strong> ${data.image_result.risk_level}</p>
        </div>

        <div class="blockchain-info">
            <h4>Blockchain Verification</h4>
            <p><strong>Transaction Hash:</strong></p>
            <code>${data.blockchain_tx}</code>
            <p><strong>Data Hash:</strong></p>
            <code>${data.data_hash}</code>
            <p><strong>Image Hash (IPFS):</strong></p>
            <code>${data.image_hash}</code>
        </div>
    `;

    resultContainer.style.display = 'block';
}