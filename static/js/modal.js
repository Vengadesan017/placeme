
    document.querySelectorAll('.open-modal-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const modalId = this.dataset.modalId;
            const modal = document.getElementById(modalId);

    
            modal.style.display = 'block';
        });
    });
    
    document.querySelectorAll('.close-modal-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            this.closest('.modal').style.display = 'none';
        });
    });
    
    

    function closeOpenedModal() {
        const openModal = document.querySelector('.modal[style*="display: block"]');
    
        if (openModal) {
            const closeBtn = openModal.querySelector('.close-modal-btn');
            if (closeBtn) {
                closeBtn.click();
            }
        }
    }