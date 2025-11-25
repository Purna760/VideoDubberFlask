const dropZone = document.getElementById('drop-zone');
const videoInput = document.getElementById('video-input');
const fileInfo = document.getElementById('file-info');
const uploadBtn = document.getElementById('upload-btn');
const uploadSection = document.getElementById('upload-section');
const progressSection = document.getElementById('progress-section');
const completeSection = document.getElementById('complete-section');
const errorSection = document.getElementById('error-section');

let selectedFile = null;

dropZone.addEventListener('click', () => {
    videoInput.click();
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

videoInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    const validTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/x-matroska'];
    const maxSize = 500 * 1024 * 1024;
    
    if (!validTypes.includes(file.type)) {
        alert('Please select a valid video file (MP4, AVI, MOV, or MKV)');
        return;
    }
    
    if (file.size > maxSize) {
        alert('File size must be less than 500MB');
        return;
    }
    
    selectedFile = file;
    document.getElementById('file-name').textContent = file.name;
    document.getElementById('file-size').textContent = `(${formatFileSize(file.size)})`;
    fileInfo.classList.remove('d-none');
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        alert('Please select a video file first');
        return;
    }
    
    const targetLanguage = document.getElementById('target-language').value;
    
    const formData = new FormData();
    formData.append('video', selectedFile);
    formData.append('target_language', targetLanguage);
    
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Uploading...';
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }
        
        const data = await response.json();
        const jobId = data.job_id;
        
        uploadSection.classList.add('d-none');
        progressSection.classList.remove('d-none');
        
        pollStatus(jobId);
        
    } catch (error) {
        alert('Error: ' + error.message);
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Start Dubbing Process';
    }
});

async function pollStatus(jobId) {
    const progressBar = document.getElementById('progress-bar');
    const statusText = document.getElementById('status-text');
    
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`/status/${jobId}`);
            const data = await response.json();
            
            progressBar.style.width = data.progress + '%';
            progressBar.textContent = data.progress + '%';
            statusText.textContent = data.step;
            
            if (data.status === 'completed') {
                clearInterval(interval);
                progressSection.classList.add('d-none');
                completeSection.classList.remove('d-none');
                document.getElementById('download-btn').href = data.download_url;
            } else if (data.status === 'failed') {
                clearInterval(interval);
                progressSection.classList.add('d-none');
                errorSection.classList.remove('d-none');
                document.getElementById('error-message').textContent = data.error || 'An unknown error occurred';
            }
        } catch (error) {
            console.error('Error polling status:', error);
        }
    }, 2000);
}
