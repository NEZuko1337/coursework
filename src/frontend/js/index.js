document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const uploadedFile = document.getElementById('uploaded-file');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const removeFile = document.getElementById('remove-file');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');

    // Handle file selection
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            displayFileDetails(file);
        }
    });

    // Handle drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragging');
    });

    uploadArea.addEventListener('dragleave', function() {
        this.classList.remove('dragging');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragging');
        
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const file = e.dataTransfer.files[0];
            fileInput.files = e.dataTransfer.files;
            displayFileDetails(file);
        }
    });

    // Remove file
    removeFile.addEventListener('click', function() {
        fileInput.value = '';
        uploadedFile.style.display = 'none';
        uploadArea.style.display = 'block';
    });

    // Analyze button
    analyzeBtn.addEventListener('click', function() {
        if (fileInput.files && fileInput.files[0]) {
            // Here you would normally send the file to the backend
            // For this demo, we'll just show the results section
            
            // Show loading state
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Обработка...';
            this.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-check"></i> Анализ завершен';
                resultsSection.style.display = 'block';
                
                // Scroll to results
                resultsSection.scrollIntoView({ behavior: 'smooth' });
                
                // Reset button after some time
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-calculator"></i> Анализировать данные';
                    this.disabled = false;
                }, 3000);
            }, 2000);
        }
    })
});