
    document.querySelectorAll('.open-modal-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const modalId = this.dataset.modalId;
            const modal = document.getElementById(modalId);
            console.log()
            modal.classList.remove('hide');
        modal.style.display = 'block';
        // Trigger reflow to enable transition
        void modal.offsetWidth;
        modal.classList.add('show');
            // modal.style.display = 'block';
        });
    });
    
    document.querySelectorAll('.close-modal-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            // this.closest('.modal').style.display = 'none';
        const modal = this.closest('.modal');
        if (modal) {
            modal.classList.remove('show');
            modal.classList.add('hide');
            setTimeout(() => {
                modal.style.display = 'none';
            }, 500); // Match your CSS animation duration
        }
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

function closeHtmxModalButton() {
    const modal = document.getElementById('HtmxModal');
    if (modal) {
        modal.style.display = 'none';
            modal.classList.remove('show');
            modal.classList.add('hide');
        document.body.classList.remove('modal-open');
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) backdrop.remove();
    }
}

function openHtmxModalButton() {
        const modal = document.getElementById('HtmxModal');
        if (modal) {
            modal.classList.remove('hide');
        modal.style.display = 'block';
        // Trigger reflow to enable transition
        void modal.offsetWidth;
        modal.classList.add('show');
                // modal.style.display = 'block';
    
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) backdrop.add();

            
        }
    }