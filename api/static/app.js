 // Ferme la page quand on clique sur "Annuler"
document.getElementById("annuler-btn").addEventListener("click", function() {
    alert("Vous pouvez fermer cette page manuellement.");
    window.close();
});

// Gère l'affichage après paiement
document.getElementById("paiement-btn").addEventListener("click", function() {
    let message = document.getElementById("paiement-message");
    let retourChat = document.getElementById("retour-chat");

    message.style.display = "block";
    this.style.backgroundColor = "#28a745";
    this.style.color = "white";
    this.innerText = "Payé ✅";
    this.disabled = true;

    retourChat.style.display = "block"; // Affiche le bouton "Retourner au chat ?"
});

// Ferme la page quand on clique sur "Retourner au chat ?"
document.getElementById("retour-chat").addEventListener("click", function() {
    alert("Vous pouvez fermer cette page manuellement.");
    window.close();
});