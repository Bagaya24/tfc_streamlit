document.getElementById('payBtn').addEventListener('click', function() {
this.disabled = true;
this.innerHTML = '<i class="ri-loader-4-line animate-spin"></i> Traitement...';
setTimeout(() => {
document.getElementById('confirmMessage').classList.remove('hidden');
this.innerHTML = '<i class="ri-checkbox-circle-line"></i> Payé';
this.classList.add('bg-opacity-80');
}, 1500);
});
document.getElementById('cancelBtn').addEventListener('click', function() {
    window.close();
});
updateTable();