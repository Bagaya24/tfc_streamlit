// Éléments DOM
const productsTable = document.getElementById('productsTable');
const productForm = document.getElementById('productForm');
const productModal = new bootstrap.Modal(document.getElementById('productModal'));
const toastElement = document.getElementById('toast');
const toast = new bootstrap.Toast(toastElement);
const modalTitle = document.querySelector('.modal-title');
const saveButton = document.getElementById('saveProduct');

// Variables globales
let products = [];
let editingProductId = null;
let categories = [];
let marques = [];
let fournisseurs = [];
let isEditing = false;

// Fonctions utilitaires
function showToast(message, success = true) {
    const toastBody = toastElement.querySelector('.toast-body');
    toastBody.textContent = message;
    toastElement.classList.remove('bg-success', 'bg-danger');
    toastElement.classList.add(success ? 'bg-success' : 'bg-danger');
    toast.show();
}

function formatDate(dateString) {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('fr-FR');
}

function resetForm() {
    productForm.reset();
    document.getElementById('productId').value = '';
    editingProductId = null;
    isEditing = false;
}

// Filtrage et recherche
function filterProducts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const selectedCategorie = document.getElementById('filterCategorie').value;
    const selectedMarque = document.getElementById('filterMarque').value;
    const selectedFournisseur = document.getElementById('filterFournisseur').value;

    const filteredProducts = products.filter(product => {
        const matchesSearch = 
            product.nom.toLowerCase().includes(searchTerm) ||
            (product.description && product.description.toLowerCase().includes(searchTerm));
        
        const matchesCategorie = !selectedCategorie || product.categorie_id.toString() === selectedCategorie;
        const matchesMarque = !selectedMarque || product.marque_id.toString() === selectedMarque;
        const matchesFournisseur = !selectedFournisseur || product.fournisseur_id.toString() === selectedFournisseur;

        return matchesSearch && matchesCategorie && matchesMarque && matchesFournisseur;
    });

    displayProducts(filteredProducts);
}

// Mise à jour des filtres
function updateFilterOptions() {
    const filterCategorie = document.getElementById('filterCategorie');
    const filterMarque = document.getElementById('filterMarque');
    const filterFournisseur = document.getElementById('filterFournisseur');

    filterCategorie.innerHTML = '<option value="">Toutes les catégories</option>' +
        categories.map(c => `<option value="${c.categorie_id}">${c.nom}</option>`).join('');

    filterMarque.innerHTML = '<option value="">Toutes les marques</option>' +
        marques.map(m => `<option value="${m.marque_id}">${m.nom}</option>`).join('');

    filterFournisseur.innerHTML = '<option value="">Tous les fournisseurs</option>' +
        fournisseurs.map(f => `<option value="${f.fournisseur_id}">${f.nom}</option>`).join('');
}

// Chargement des données de référence
async function loadReferenceData() {
    try {
        const [categoriesResponse, marquesResponse, fournisseursResponse] = await Promise.all([
            fetch('/api/categories'),
            fetch('/api/marques'),
            fetch('/api/fournisseurs')
        ]);

        categories = await categoriesResponse.json();
        marques = await marquesResponse.json();
        fournisseurs = await fournisseursResponse.json();

        updateSelectOptions();
        updateFilterOptions();
    } catch (error) {
        console.error('Erreur lors du chargement des données de référence:', error);
        showToast('Erreur lors du chargement des données de référence', false);
    }
}

function updateSelectOptions() {
    const categorieSelect = document.getElementById('categorie');
    const marqueSelect = document.getElementById('marque');
    const fournisseurSelect = document.getElementById('fournisseur');

    categorieSelect.innerHTML = '<option value="">Sélectionner une catégorie</option>' +
        categories.map(c => `<option value="${c.categorie_id}">${c.nom}</option>`).join('');

    marqueSelect.innerHTML = '<option value="">Sélectionner une marque</option>' +
        marques.map(m => `<option value="${m.marque_id}">${m.nom}</option>`).join('');

    fournisseurSelect.innerHTML = '<option value="">Sélectionner un fournisseur</option>' +
        fournisseurs.map(f => `<option value="${f.fournisseur_id}">${f.nom}</option>`).join('');
}

// Chargement et affichage des produits
async function loadProducts() {
    try {
        const response = await fetch('/api/produits');
        products = await response.json();
        filterProducts(); // Utilise la fonction de filtrage pour l'affichage
    } catch (error) {
        console.error('Erreur lors du chargement des produits:', error);
        showToast('Erreur lors du chargement des produits', false);
    }
}

function displayProducts(productsToDisplay) {
    const tbody = productsTable.querySelector('tbody');
    tbody.innerHTML = productsToDisplay.map(product => {
        const categorie = categories.find(c => c.categorie_id === product.categorie_id)?.nom || '';
        const marque = marques.find(m => m.marque_id === product.marque_id)?.nom || '';
        const fournisseur = fournisseurs.find(f => f.fournisseur_id === product.fournisseur_id)?.nom || '';

        return `
            <tr>
                <td>${product.product_id}</td>
                <td>${product.nom}</td>
                <td>${product.description || ''}</td>
                <td>${product.prix.toFixed(2)} $</td>
                <td>${product.quantité_en_stock}</td>
                <td>${categorie}</td>
                <td>${marque}</td>
                <td>${fournisseur}</td>
                <td>${formatDate(product.date_expiration)}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="editProduct(${product.product_id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteProduct(${product.product_id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Préparation pour l'ajout d'un nouveau produit
function prepareAddProduct() {
    resetForm();
    modalTitle.textContent = 'Ajouter un Produit';
    productModal.show();
}

// Édition d'un produit
async function editProduct(productId) {
    try {
        const response = await fetch(`/api/produits/${productId}`);
        const product = await response.json();
        
        isEditing = true;
        editingProductId = product.product_id;
        modalTitle.textContent = 'Modifier le Produit';
        
        document.getElementById('productId').value = product.product_id;
        document.getElementById('nom').value = product.nom;
        document.getElementById('description').value = product.description || '';
        document.getElementById('prix').value = product.prix;
        document.getElementById('quantite').value = product.quantité_en_stock;
        document.getElementById('categorie').value = product.categorie_id || '';
        document.getElementById('marque').value = product.marque_id || '';
        document.getElementById('fournisseur').value = product.fournisseur_id || '';
        document.getElementById('dateExpiration').value = product.date_expiration ? 
            new Date(product.date_expiration).toISOString().split('T')[0] : '';
        
        productModal.show();
    } catch (error) {
        console.error('Erreur lors du chargement du produit:', error);
        showToast('Erreur lors du chargement du produit', false);
    }
}

// Suppression d'un produit
async function deleteProduct(productId) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce produit ?')) return;
    
    try {
        const response = await fetch(`/api/produits/${productId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Produit supprimé avec succès');
            loadProducts();
        } else {
            throw new Error('Erreur lors de la suppression');
        }
    } catch (error) {
        console.error('Erreur lors de la suppression du produit:', error);
        showToast('Erreur lors de la suppression du produit', false);
    }
}

// Sauvegarde d'un produit (ajout ou modification)
async function saveProduct() {
    const productData = {
        nom: document.getElementById('nom').value,
        description: document.getElementById('description').value,
        prix: parseFloat(document.getElementById('prix').value),
        quantite_en_stock: parseInt(document.getElementById('quantite').value),
        categorie_id: document.getElementById('categorie').value || null,
        marque_id: document.getElementById('marque').value || null,
        fournisseur_id: document.getElementById('fournisseur').value || null,
        date_expiration: document.getElementById('dateExpiration').value || null
    };

    try {
        const url = isEditing ? `/api/produits/${editingProductId}` : '/api/produits';
        const method = isEditing ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData)
        });

        if (response.ok) {
            showToast(`Produit ${isEditing ? 'modifié' : 'ajouté'} avec succès`);
            productModal.hide();
            resetForm();
            loadProducts();
        } else {
            throw new Error('Erreur lors de la sauvegarde');
        }
    } catch (error) {
        console.error('Erreur lors de la sauvegarde du produit:', error);
        showToast('Erreur lors de la sauvegarde du produit', false);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    loadReferenceData();
    loadProducts();

    // Écouteurs pour la recherche et les filtres
    document.getElementById('searchInput').addEventListener('input', filterProducts);
    document.getElementById('filterCategorie').addEventListener('change', filterProducts);
    document.getElementById('filterMarque').addEventListener('change', filterProducts);
    document.getElementById('filterFournisseur').addEventListener('change', filterProducts);
});

// Gestionnaire pour le bouton "Ajouter un Produit"
document.querySelector('[data-bs-target="#productModal"]').addEventListener('click', prepareAddProduct);

// Gestionnaire pour le bouton "Enregistrer"
saveButton.addEventListener('click', saveProduct);

// Réinitialisation du formulaire à la fermeture du modal
document.getElementById('productModal').addEventListener('hidden.bs.modal', resetForm);
