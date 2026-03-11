let currentRecipeId = null;
let allRecipes = [];

// DOM Elements
const recipesGrid = document.getElementById('recipesGrid');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const addRecipeBtn = document.getElementById('addRecipeBtn');
const importUrlBtn = document.getElementById('importUrlBtn');

// Modals
const recipeModal = document.getElementById('recipeModal');
const editModal = document.getElementById('editModal');
const importModal = document.getElementById('importModal');

// Close buttons
const closeButtons = document.querySelectorAll('.close');
closeButtons.forEach(btn => {
    btn.onclick = function() {
        closeAllModals();
    };
});

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        closeAllModals();
    }
};

function closeAllModals() {
    recipeModal.style.display = 'none';
    editModal.style.display = 'none';
    importModal.style.display = 'none';
}

// Load all recipes on page load
document.addEventListener('DOMContentLoaded', () => {
    loadRecipes();
});

// Search functionality
searchBtn.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        performSearch();
    }
});

clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    loadRecipes();
});

function performSearch() {
    const query = searchInput.value.trim();
    if (query) {
        searchRecipes(query);
    } else {
        loadRecipes();
    }
}

// Add recipe button
addRecipeBtn.addEventListener('click', () => {
    openAddRecipeModal();
});

// Import URL button
importUrlBtn.addEventListener('click', () => {
    openImportModal();
});

// Recipe form submission
document.getElementById('recipeForm').addEventListener('submit', (e) => {
    e.preventDefault();
    saveRecipe();
});

// Cancel edit button
document.getElementById('cancelEditBtn').addEventListener('click', () => {
    editModal.style.display = 'none';
});

// Import form submission
document.getElementById('importForm').addEventListener('submit', (e) => {
    e.preventDefault();
    importRecipeFromUrl();
});

// Cancel import button
document.getElementById('cancelImportBtn').addEventListener('click', () => {
    importModal.style.display = 'none';
});

// API Functions
async function loadRecipes() {
    try {
        showLoading();
        const response = await fetch('/api/recipes');
        const recipes = await response.json();
        allRecipes = recipes;
        displayRecipes(recipes);
    } catch (error) {
        console.error('Error loading recipes:', error);
        showError('Failed to load recipes');
    }
}

async function searchRecipes(query) {
    try {
        showLoading();
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const recipes = await response.json();
        displayRecipes(recipes);
    } catch (error) {
        console.error('Error searching recipes:', error);
        showError('Failed to search recipes');
    }
}

async function getRecipe(id) {
    try {
        const response = await fetch(`/api/recipes/${id}`);
        const recipe = await response.json();
        return recipe;
    } catch (error) {
        console.error('Error getting recipe:', error);
        return null;
    }
}

async function saveRecipe() {
    const recipe = {
        name: document.getElementById('recipeName').value,
        description: document.getElementById('recipeDescription').value,
        prep_time: document.getElementById('recipePrepTime').value,
        cook_time: document.getElementById('recipeCookTime').value,
        servings: document.getElementById('recipeServings').value,
        ingredients: document.getElementById('recipeIngredients').value.split('\n').filter(i => i.trim()),
        instructions: document.getElementById('recipeInstructions').value.split('\n').filter(i => i.trim()),
        tags: document.getElementById('recipeTags').value.split(',').map(t => t.trim()).filter(t => t),
        image_url: document.getElementById('recipeImageUrl').value,
        source_url: document.getElementById('recipeSourceUrl').value
    };

    try {
        let response;
        if (currentRecipeId) {
            // Update existing recipe
            response = await fetch(`/api/recipes/${currentRecipeId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(recipe)
            });
        } else {
            // Create new recipe
            response = await fetch('/api/recipes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(recipe)
            });
        }

        if (response.ok) {
            editModal.style.display = 'none';
            loadRecipes();
            resetForm();
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        console.error('Error saving recipe:', error);
        alert('Failed to save recipe');
    }
}

async function deleteRecipe(id) {
    if (!confirm('Are you sure you want to delete this recipe?')) {
        return;
    }

    try {
        const response = await fetch(`/api/recipes/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            recipeModal.style.display = 'none';
            loadRecipes();
        } else {
            alert('Failed to delete recipe');
        }
    } catch (error) {
        console.error('Error deleting recipe:', error);
        alert('Failed to delete recipe');
    }
}

async function importRecipeFromUrl() {
    const url = document.getElementById('importUrl').value;
    const statusDiv = document.getElementById('importStatus');

    statusDiv.className = 'import-status loading';
    statusDiv.textContent = 'Importing recipe... This may take a few seconds.';

    try {
        const response = await fetch('/api/parse-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const result = await response.json();

        if (response.ok) {
            statusDiv.className = 'import-status success';
            statusDiv.textContent = 'Recipe imported successfully! Opening editor...';

            setTimeout(() => {
                importModal.style.display = 'none';
                openAddRecipeModal(result);
                statusDiv.className = 'import-status';
                statusDiv.textContent = '';
                document.getElementById('importUrl').value = '';
            }, 1500);
        } else {
            statusDiv.className = 'import-status error';
            statusDiv.textContent = 'Error: ' + result.error;
        }
    } catch (error) {
        console.error('Error importing recipe:', error);
        statusDiv.className = 'import-status error';
        statusDiv.textContent = 'Failed to import recipe: ' + error.message;
    }
}

// Display Functions
function displayRecipes(recipes) {
    if (recipes.length === 0) {
        recipesGrid.innerHTML = '<div class="empty-state">No recipes found. Add your first recipe!</div>';
        return;
    }

    recipesGrid.innerHTML = recipes.map(recipe => createRecipeCard(recipe)).join('');

    // Add click listeners
    document.querySelectorAll('.recipe-card').forEach(card => {
        card.addEventListener('click', () => {
            const id = card.dataset.id;
            showRecipeDetails(id);
        });
    });
}

function createRecipeCard(recipe) {
    const tags = recipe.tags || [];
    const tagsHtml = tags.map(tag => `<span class="tag">${tag}</span>`).join('');
    
    const imageUrl = recipe.image_url || '';
    const imageHtml = imageUrl ? 
        `<img src="${imageUrl}" alt="${recipe.name}" class="recipe-image" onerror="this.style.display='none'">` : 
        '<div class="recipe-image"></div>';

    const meta = [];
    if (recipe.prep_time) meta.push(`⏱️ ${recipe.prep_time}`);
    if (recipe.cook_time) meta.push(`🔥 ${recipe.cook_time}`);
    if (recipe.servings) meta.push(`🍽️ ${recipe.servings}`);

    return `
        <div class="recipe-card" data-id="${recipe.id}">
            ${imageHtml}
            <div class="recipe-card-content">
                <h3>${recipe.name}</h3>
                <p>${recipe.description || 'No description available.'}</p>
                ${meta.length > 0 ? `<div class="recipe-meta">${meta.join(' • ')}</div>` : ''}
                ${tagsHtml ? `<div class="recipe-tags">${tagsHtml}</div>` : ''}
            </div>
        </div>
    `;
}

async function showRecipeDetails(id) {
    const recipe = await getRecipe(id);
    if (!recipe) return;

    const ingredients = recipe.ingredients || [];
    const instructions = recipe.instructions || [];
    const tags = recipe.tags || [];

    const imageHtml = recipe.image_url ? 
        `<img src="${recipe.image_url}" alt="${recipe.name}" class="recipe-detail-image" onerror="this.style.display='none'">` : '';

    const meta = [];
    if (recipe.prep_time) meta.push(`⏱️ Prep: ${recipe.prep_time}`);
    if (recipe.cook_time) meta.push(`🔥 Cook: ${recipe.cook_time}`);
    if (recipe.servings) meta.push(`🍽️ Servings: ${recipe.servings}`);

    const tagsHtml = tags.map(tag => `<span class="tag">${tag}</span>`).join('');

    const detailsHtml = `
        <div class="recipe-detail-header">
            <h2>${recipe.name}</h2>
            ${recipe.description ? `<p>${recipe.description}</p>` : ''}
            ${meta.length > 0 ? `<div class="recipe-meta" style="margin-top: 10px;">${meta.join(' • ')}</div>` : ''}
            ${tagsHtml ? `<div class="recipe-tags" style="margin-top: 10px;">${tagsHtml}</div>` : ''}
        </div>

        ${imageHtml}

        <div class="recipe-detail-section">
            <h3>📋 Ingredients</h3>
            <ul>
                ${ingredients.map(ing => `<li>${ing}</li>`).join('')}
            </ul>
        </div>

        <div class="recipe-detail-section">
            <h3>👨‍🍳 Instructions</h3>
            <ol>
                ${instructions.map(inst => `<li>${inst}</li>`).join('')}
            </ol>
        </div>

        ${recipe.source_url ? `
            <div class="recipe-detail-section">
                <h3>🔗 Source</h3>
                <a href="${recipe.source_url}" target="_blank">${recipe.source_url}</a>
            </div>
        ` : ''}

        <div class="recipe-actions">
            <button onclick="editRecipe(${recipe.id})" class="btn btn-primary">Edit</button>
            <button onclick="deleteRecipe(${recipe.id})" class="btn btn-danger">Delete</button>
        </div>
    `;

    document.getElementById('recipeDetails').innerHTML = detailsHtml;
    recipeModal.style.display = 'block';
}

function openAddRecipeModal(prefilledData = null) {
    currentRecipeId = null;
    document.getElementById('editModalTitle').textContent = 'Add Recipe';
    resetForm();

    if (prefilledData) {
        document.getElementById('recipeName').value = prefilledData.name || '';
        document.getElementById('recipeDescription').value = prefilledData.description || '';
        document.getElementById('recipePrepTime').value = prefilledData.prep_time || '';
        document.getElementById('recipeCookTime').value = prefilledData.cook_time || '';
        document.getElementById('recipeServings').value = prefilledData.servings || '';
        document.getElementById('recipeIngredients').value = (prefilledData.ingredients || []).join('\n');
        document.getElementById('recipeInstructions').value = (prefilledData.instructions || []).join('\n');
        document.getElementById('recipeTags').value = (prefilledData.tags || []).join(', ');
        document.getElementById('recipeImageUrl').value = prefilledData.image_url || '';
        document.getElementById('recipeSourceUrl').value = prefilledData.source_url || '';
    }

    editModal.style.display = 'block';
}

async function editRecipe(id) {
    const recipe = await getRecipe(id);
    if (!recipe) return;

    currentRecipeId = id;
    document.getElementById('editModalTitle').textContent = 'Edit Recipe';

    document.getElementById('recipeName').value = recipe.name || '';
    document.getElementById('recipeDescription').value = recipe.description || '';
    document.getElementById('recipePrepTime').value = recipe.prep_time || '';
    document.getElementById('recipeCookTime').value = recipe.cook_time || '';
    document.getElementById('recipeServings').value = recipe.servings || '';
    document.getElementById('recipeIngredients').value = (recipe.ingredients || []).join('\n');
    document.getElementById('recipeInstructions').value = (recipe.instructions || []).join('\n');
    document.getElementById('recipeTags').value = (recipe.tags || []).join(', ');
    document.getElementById('recipeImageUrl').value = recipe.image_url || '';
    document.getElementById('recipeSourceUrl').value = recipe.source_url || '';

    recipeModal.style.display = 'none';
    editModal.style.display = 'block';
}

function openImportModal() {
    document.getElementById('importUrl').value = '';
    document.getElementById('importStatus').className = 'import-status';
    document.getElementById('importStatus').textContent = '';
    importModal.style.display = 'block';
}

function resetForm() {
    document.getElementById('recipeForm').reset();
    currentRecipeId = null;
}

function showLoading() {
    recipesGrid.innerHTML = '<div class="loading-spinner">Loading recipes...</div>';
}

function showError(message) {
    recipesGrid.innerHTML = `<div class="empty-state">${message}</div>`;
}
