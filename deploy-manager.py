#!/usr/bin/env python3
"""
Garden Deploy Manager v2.2 - GitHub Fork System
Project Deployment and Production Manager

A complete deployment infrastructure for GARDEN projects that:
- Downloads GARDEN DNA from GitHub repository
- Creates true project forks with core files
- Supports multiple project templates
- Provides production deployment capabilities
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import glob
from pathlib import Path
from datetime import datetime
import zipfile
import urllib.request

class GardenDeployManager:
    def __init__(self):
        self.github_repo = "https://github.com/scottloeb/garden"
        self.current_dir = Path.cwd()
        
        # Core GARDEN DNA files (comprehensive v2.2)
        self.core_files = [
            # All contexts (entire folder)
            'contexts/',
            
            # Development tools  
            'toolshed/nodepad-4.0.0.html',
            'generated/modulegenerator_v2/',
            'generated/README.md',
            'module-generators/',
            'sunflower/',
            
            # Project documentation
            'CONTRIBUTING.md',
            'README.md', 
            'requirements.txt',
            '.gitignore'
        ]
        
        # Project templates
        self.templates = {
            "Recipe NodePad": {
                "description": "Complete recipe management with 4x6 cards and shopping lists",
                "main_file": "recipe-nodepad.html",
                "contexts": ["CIT_RecipeNodePad.md"],
                "template_type": "nodepad"
            },
            "Idea Capture": {
                "description": "Lightning-fast brain dump with auto-categorization",
                "main_file": "idea-capture.html", 
                "contexts": ["CIT_IdeaCapture.md"],
                "template_type": "nodepad"
            },
            "Budget Manager": {
                "description": "Visual budget planning with CSV import",
                "main_file": "budget-nodepad.html",
                "contexts": ["CIT_BudgetNodePad.md"],
                "template_type": "nodepad"
            },
            "Basic NodePad": {
                "description": "Clean NodePad 4.0.0 starting point",
                "main_file": "nodepad.html",
                "contexts": [],
                "template_type": "nodepad"
            }
        }

    def show_banner(self):
        print("\n" + "="*60)
        print("🌱 GARDEN Deploy Manager v2.2")
        print("   Project Deployment and Production Manager")
        print("="*60)
        print("🧬 GitHub Fork System - Downloads GARDEN DNA")
        print("🚀 Production Ready - Vercel/GitHub Integration")
        print("📋 Complete Templates - Recipe, Ideas, Budget")
        print("="*60 + "\n")

    def show_menu(self):
        print("🎯 Deployment Options:")
        print("0. 🌱 Fork New Garden Project")
        print("1. 🚀 Deploy Existing Project to Vercel")
        print("2. 🔍 Test GitHub Connection")
        print("3. 📋 Show Available Templates")
        print("4. 🧬 Show Core Files List")
        print("5. ❌ Exit")
        return input("\n👉 Select option (0-5): ").strip()

    def test_github_connection(self):
        """Test if we can connect to the GitHub repository"""
        print("🔍 Testing GitHub connection...")
        try:
            # Test download of a small file
            test_url = f"{self.github_repo}/raw/main/README.md"
            with urllib.request.urlopen(test_url) as response:
                content = response.read().decode('utf-8')
            
            print(f"✅ Successfully connected to {self.github_repo}")
            print(f"📄 README.md preview: {content[:100]}...")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to GitHub: {str(e)}")
            return False

    def download_garden_repo(self):
        """Download the GARDEN repository as a zip file"""
        print("📥 Downloading GARDEN repository...")
        try:
            zip_url = f"{self.github_repo}/archive/refs/heads/main.zip"
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                with urllib.request.urlopen(zip_url) as response:
                    tmp_file.write(response.read())
                
                zip_path = tmp_file.name
            
            # Extract to temporary directory
            extract_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Find the extracted garden directory
            garden_dir = None
            for item in os.listdir(extract_dir):
                if item.startswith('garden'):
                    garden_dir = os.path.join(extract_dir, item)
                    break
            
            if not garden_dir:
                raise Exception("Could not find garden directory in downloaded zip")
            
            print(f"✅ Downloaded and extracted to: {garden_dir}")
            return garden_dir
            
        except Exception as e:
            print(f"❌ Failed to download repository: {str(e)}")
            return None
        finally:
            # Clean up zip file
            if 'zip_path' in locals():
                try:
                    os.unlink(zip_path)
                except:
                    pass

    def copy_core_files(self, source_dir, target_dir):
        """Copy core GARDEN files from source to target directory"""
        print("📋 Copying core GARDEN files...")
        copied_count = 0
        
        for core_file in self.core_files:
            source_path = os.path.join(source_dir, core_file)
            target_path = os.path.join(target_dir, core_file)
            
            try:
                if os.path.isdir(source_path):
                    # Copy entire directory
                    if os.path.exists(target_path):
                        shutil.rmtree(target_path)
                    shutil.copytree(source_path, target_path)
                    file_count = sum([len(files) for r, d, files in os.walk(target_path)])
                    print(f"  ✓ {core_file}/ ({file_count} files)")
                    copied_count += file_count
                elif os.path.isfile(source_path):
                    # Copy single file
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(source_path, target_path)
                    print(f"  ✓ {core_file}")
                    copied_count += 1
                else:
                    print(f"  ⚠️ Not found: {core_file}")
            except Exception as e:
                print(f"  ❌ Error copying {core_file}: {str(e)}")
        
        print(f"📦 Copied {copied_count} core files/directories")
        return copied_count > 0

    def create_template_file(self, template_name, project_dir):
        """Create the main template file for the project"""
        template = self.templates[template_name]
        main_file_path = os.path.join(project_dir, template["main_file"])
        
        if template_name == "Recipe NodePad":
            content = self.get_recipe_nodepad_template()
        elif template_name == "Idea Capture":
            content = self.get_idea_capture_template()
        elif template_name == "Budget Manager":
            content = self.get_budget_manager_template()
        else:
            content = self.get_basic_nodepad_template()
        
        with open(main_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ {template['main_file']} (template)")

    def get_recipe_nodepad_template(self):
        """Complete Recipe NodePad implementation"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipe NodePad</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: system-ui, -apple-system, sans-serif; 
            background: #f8f9fa; 
            color: #333;
        }
        
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 20px;
            height: 100vh;
        }
        
        .sidebar {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow-y: auto;
        }
        
        .main-content {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }
        
        .header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .emoji { font-size: 32px; }
        
        h1 { 
            color: #2c3e50;
            font-size: 24px;
            font-weight: 600;
        }
        
        .subtitle {
            color: #6c757d;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #495057;
        }
        
        input, textarea, select {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            font-size: 14px;
        }
        
        textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        .btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: background 0.2s;
        }
        
        .btn:hover {
            background: #0056b3;
        }
        
        .btn-secondary {
            background: #6c757d;
        }
        
        .btn-secondary:hover {
            background: #545b62;
        }
        
        .recipe-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .recipe-item {
            padding: 10px;
            margin-bottom: 8px;
            background: #f8f9fa;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .recipe-item:hover {
            background: #e9ecef;
        }
        
        .recipe-item.active {
            background: #007bff;
            color: white;
        }
        
        .recipe-title {
            font-weight: 500;
            margin-bottom: 2px;
        }
        
        .recipe-meta {
            font-size: 12px;
            color: #6c757d;
        }
        
        .recipe-item.active .recipe-meta {
            color: #bdd7ff;
        }
        
        .ingredients-section, .instructions-section {
            margin-bottom: 20px;
        }
        
        .section-title {
            font-weight: 600;
            margin-bottom: 10px;
            color: #495057;
        }
        
        .ingredient-item, .instruction-item {
            display: flex;
            gap: 10px;
            margin-bottom: 8px;
            align-items: flex-start;
        }
        
        .ingredient-item input[type="number"] {
            width: 80px;
        }
        
        .ingredient-item input[type="text"]:first-of-type {
            width: 80px;
        }
        
        .ingredient-item input[type="text"]:last-of-type {
            flex: 1;
        }
        
        .instruction-item input {
            flex: 1;
        }
        
        .remove-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }
        
        .add-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            margin-top: 5px;
        }
        
        .actions {
            display: flex;
            gap: 10px;
            margin-top: auto;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }
        
        .print-card {
            width: 6in;
            height: 4in;
            background: white;
            border: 1px solid #ddd;
            padding: 0.25in;
            margin: 20px auto;
            font-size: 10pt;
            line-height: 1.2;
            page-break-after: always;
        }
        
        @media print {
            body { background: white; }
            .container { display: none; }
            .print-card { 
                display: block !important;
                margin: 0;
                border: none;
                box-shadow: none;
            }
        }
        
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
                gap: 10px;
                padding: 10px;
            }
            
            .sidebar {
                order: 2;
                max-height: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="header">
                <span class="emoji">🍳</span>
                <div>
                    <h2 style="font-size: 18px; margin-bottom: 2px;">Recipe Collection</h2>
                    <div class="subtitle">NodePad Kitchen</div>
                </div>
            </div>
            
            <button class="btn" onclick="createNewRecipe()" style="width: 100%; margin-bottom: 15px;">
                + New Recipe
            </button>
            
            <div class="recipe-list" id="recipeList">
                <!-- Recipes will be populated here -->
            </div>
            
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e9ecef;">
                <button class="btn btn-secondary" onclick="exportRecipes()" style="width: 100%; margin-bottom: 8px;">
                    📤 Export Recipes
                </button>
                <input type="file" id="importFile" accept=".json" style="display: none;" onchange="importRecipes(event)">
                <button class="btn btn-secondary" onclick="document.getElementById('importFile').click()" style="width: 100%;">
                    📥 Import Recipes
                </button>
            </div>
        </div>
        
        <div class="main-content">
            <div class="header">
                <span class="emoji">📝</span>
                <div>
                    <h1 id="recipeTitle">New Recipe</h1>
                    <div class="subtitle">Recipe Details</div>
                </div>
            </div>
            
            <div id="recipeForm">
                <div class="form-group">
                    <label for="recipeName">Recipe Name</label>
                    <input type="text" id="recipeName" placeholder="Enter recipe name..." onchange="saveRecipe()">
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                    <div class="form-group">
                        <label for="servings">Servings</label>
                        <input type="number" id="servings" placeholder="4" onchange="saveRecipe()">
                    </div>
                    <div class="form-group">
                        <label for="prepTime">Prep Time</label>
                        <input type="text" id="prepTime" placeholder="15 min" onchange="saveRecipe()">
                    </div>
                    <div class="form-group">
                        <label for="cookTime">Cook Time</label>
                        <input type="text" id="cookTime" placeholder="30 min" onchange="saveRecipe()">
                    </div>
                </div>
                
                <div class="ingredients-section">
                    <div class="section-title">🥕 Ingredients</div>
                    <div id="ingredientsList">
                        <!-- Ingredients will be populated here -->
                    </div>
                    <button class="add-btn" onclick="addIngredient()">+ Add Ingredient</button>
                </div>
                
                <div class="instructions-section">
                    <div class="section-title">👨‍🍳 Instructions</div>
                    <div id="instructionsList">
                        <!-- Instructions will be populated here -->
                    </div>
                    <button class="add-btn" onclick="addInstruction()">+ Add Step</button>
                </div>
            </div>
            
            <div class="actions">
                <button class="btn" onclick="printRecipeCard()">🖨️ Print 4x6 Card</button>
                <button class="btn btn-secondary" onclick="generateShoppingList()">🛒 Shopping List</button>
                <button class="btn btn-secondary" onclick="deleteCurrentRecipe()">🗑️ Delete Recipe</button>
            </div>
        </div>
    </div>
    
    <div id="printCard" class="print-card" style="display: none;">
        <!-- Print card content will be populated here -->
    </div>

    <script>
        let recipes = [];
        let currentRecipeId = null;
        
        // Load recipes from localStorage on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadRecipes();
            if (recipes.length === 0) {
                createNewRecipe();
            } else {
                selectRecipe(recipes[0].id);
            }
        });
        
        function generateId() {
            return Date.now().toString(36) + Math.random().toString(36).substr(2);
        }
        
        function createNewRecipe() {
            const newRecipe = {
                id: generateId(),
                name: 'New Recipe',
                servings: 4,
                prepTime: '',
                cookTime: '',
                ingredients: [{ quantity: '', unit: '', name: '' }],
                instructions: ['']
            };
            
            recipes.push(newRecipe);
            selectRecipe(newRecipe.id);
            saveRecipes();
            renderRecipeList();
            
            // Focus on recipe name input
            document.getElementById('recipeName').focus();
        }
        
        function selectRecipe(id) {
            currentRecipeId = id;
            const recipe = recipes.find(r => r.id === id);
            if (!recipe) return;
            
            // Update form
            document.getElementById('recipeName').value = recipe.name;
            document.getElementById('servings').value = recipe.servings;
            document.getElementById('prepTime').value = recipe.prepTime;
            document.getElementById('cookTime').value = recipe.cookTime;
            document.getElementById('recipeTitle').textContent = recipe.name;
            
            renderIngredients(recipe.ingredients);
            renderInstructions(recipe.instructions);
            renderRecipeList();
        }
        
        function renderRecipeList() {
            const list = document.getElementById('recipeList');
            list.innerHTML = '';
            
            recipes.forEach(recipe => {
                const item = document.createElement('div');
                item.className = `recipe-item ${recipe.id === currentRecipeId ? 'active' : ''}`;
                item.onclick = () => selectRecipe(recipe.id);
                
                item.innerHTML = `
                    <div class="recipe-title">${recipe.name}</div>
                    <div class="recipe-meta">${recipe.servings} servings • ${recipe.ingredients.length} ingredients</div>
                `;
                
                list.appendChild(item);
            });
        }
        
        function renderIngredients(ingredients) {
            const container = document.getElementById('ingredientsList');
            container.innerHTML = '';
            
            ingredients.forEach((ingredient, index) => {
                const item = document.createElement('div');
                item.className = 'ingredient-item';
                item.innerHTML = `
                    <input type="number" placeholder="1" value="${ingredient.quantity}" 
                           onchange="updateIngredient(${index}, 'quantity', this.value)" step="0.25">
                    <input type="text" placeholder="cup" value="${ingredient.unit}"
                           onchange="updateIngredient(${index}, 'unit', this.value)">
                    <input type="text" placeholder="ingredient name" value="${ingredient.name}"
                           onchange="updateIngredient(${index}, 'name', this.value)">
                    <button class="remove-btn" onclick="removeIngredient(${index})">×</button>
                `;
                container.appendChild(item);
            });
        }
        
        function renderInstructions(instructions) {
            const container = document.getElementById('instructionsList');
            container.innerHTML = '';
            
            instructions.forEach((instruction, index) => {
                const item = document.createElement('div');
                item.className = 'instruction-item';
                item.innerHTML = `
                    <span style="font-weight: 500; margin-right: 8px; color: #6c757d;">${index + 1}.</span>
                    <input type="text" placeholder="Add cooking instruction..." value="${instruction}"
                           onchange="updateInstruction(${index}, this.value)">
                    <button class="remove-btn" onclick="removeInstruction(${index})">×</button>
                `;
                container.appendChild(item);
            });
        }
        
        function addIngredient() {
            const recipe = recipes.find(r => r.id === currentRecipeId);
            recipe.ingredients.push({ quantity: '', unit: '', name: '' });
            renderIngredients(recipe.ingredients);
            saveRecipe();
        }
        
        function addInstruction() {
            const recipe = recipes.find(r => r.id === currentRecipeId);
            recipe.instructions.push('');
            renderInstructions(recipe.instructions);
            saveRecipe();
        }
        
        function updateIngredient(index, field, value) {
            const recipe = recipes.find(r => r.id === currentRecipeId);
            recipe.ingredients[index][field] = value;
            saveRecipe();
        }
        
        function updateInstruction(index, value) {
            const recipe = recipes.find(r => r.id === currentRecipeId);
            recipe.instructions[index] = value;
            saveRecipe();
        }
        
        function removeIngredient(index) {
            const recipe = recipes.find(r => r.id === currentRecipeId);
            recipe.ingredients.splice(index, 1);
            if (recipe.ingredients.length === 0) {
                recipe.ingredients.push({ quantity: '', unit: '', name: '' });
            }
            renderIngredients(recipe.ingredients);
            saveRecipe();
        }
        
        function removeInstruction(index) {
            const recipe = recipes.find(r => r.id === currentRecipeId);
            recipe.instructions.splice(index, 1);
            if (recipe.instructions.length === 0) {
                recipe.instructions.push('');
            }
            renderInstructions(recipe.instructions);
            saveRecipe();
        }
        
        function saveRecipe() {
            const recipe = recipes.find(r => r.id === currentRecipeId);
            if (!recipe) return;
            
            recipe.name = document.getElementById('recipeName').value || 'New Recipe';
            recipe.servings = parseInt(document.getElementById('servings').value) || 4;
            recipe.prepTime = document.getElementById('prepTime').value;
            recipe.cookTime = document.getElementById('cookTime').value;
            
            document.getElementById('recipeTitle').textContent = recipe.name;
            
            saveRecipes();
            renderRecipeList();
        }
        
        function deleteCurrentRecipe() {
            if (!currentRecipeId || recipes.length === 1) return;
            
            if (confirm('Delete this recipe?')) {
                recipes = recipes.filter(r => r.id !== currentRecipeId);
                
                if (recipes.length > 0) {
                    selectRecipe(recipes[0].id);
                } else {
                    createNewRecipe();
                }
                
                saveRecipes();
                renderRecipeList();
            }
        }
        
        function printRecipeCard() {
            const recipe = recipes.find(r => r.id === currentRecipeId);
            if (!recipe) return;
            
            const printCard = document.getElementById('printCard');
            printCard.innerHTML = `
                <div style="border-bottom: 2px solid #333; margin-bottom: 8px; padding-bottom: 4px;">
                    <h3 style="margin: 0; font-size: 14pt;">${recipe.name}</h3>
                    <div style="font-size: 8pt; color: #666;">
                        Serves ${recipe.servings} • Prep: ${recipe.prepTime} • Cook: ${recipe.cookTime}
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; height: calc(100% - 40px);">
                    <div>
                        <h4 style="margin: 0 0 6px 0; font-size: 10pt; border-bottom: 1px solid #ccc;">Ingredients</h4>
                        <div style="font-size: 8pt; line-height: 1.3;">
                            ${recipe.ingredients.map(ing => 
                                `<div>• ${ing.quantity} ${ing.unit} ${ing.name}</div>`
                            ).join('')}
                        </div>
                    </div>
                    
                    <div>
                        <h4 style="margin: 0 0 6px 0; font-size: 10pt; border-bottom: 1px solid #ccc;">Instructions</h4>
                        <div style="font-size: 8pt; line-height: 1.3;">
                            ${recipe.instructions.map((inst, i) => 
                                `<div style="margin-bottom: 4px;"><strong>${i+1}.</strong> ${inst}</div>`
                            ).join('')}
                        </div>
                    </div>
                </div>
            `;
            
            printCard.style.display = 'block';
            window.print();
            printCard.style.display = 'none';
        }
        
        function generateShoppingList() {
            const allIngredients = {};
            
            recipes.forEach(recipe => {
                recipe.ingredients.forEach(ing => {
                    if (ing.name.trim()) {
                        const key = ing.name.toLowerCase();
                        if (!allIngredients[key]) {
                            allIngredients[key] = [];
                        }
                        allIngredients[key].push(`${ing.quantity} ${ing.unit}`.trim());
                    }
                });
            });
            
            let shoppingList = "🛒 Shopping List\\n\\n";
            Object.keys(allIngredients).sort().forEach(ingredient => {
                const quantities = allIngredients[ingredient].join(', ');
                shoppingList += `□ ${ingredient} (${quantities})\\n`;
            });
            
            // Create a new window with the shopping list
            const newWindow = window.open('', '_blank');
            newWindow.document.write(`
                <html>
                    <head><title>Shopping List</title></head>
                    <body style="font-family: system-ui; padding: 20px; line-height: 1.6;">
                        <pre style="white-space: pre-wrap;">${shoppingList}</pre>
                        <button onclick="window.print()" style="margin-top: 20px; padding: 10px 20px;">Print List</button>
                    </body>
                </html>
            `);
        }
        
        function saveRecipes() {
            localStorage.setItem('recipeNodePadData', JSON.stringify(recipes));
        }
        
        function loadRecipes() {
            const saved = localStorage.getItem('recipeNodePadData');
            if (saved) {
                recipes = JSON.parse(saved);
            }
            renderRecipeList();
        }
        
        function exportRecipes() {
            const dataStr = JSON.stringify(recipes, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `recipes-${new Date().toISOString().split('T')[0]}.json`;
            link.click();
        }
        
        function importRecipes(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const importedRecipes = JSON.parse(e.target.result);
                    
                    if (confirm(`Import ${importedRecipes.length} recipes? This will merge with existing recipes.`)) {
                        importedRecipes.forEach(recipe => {
                            recipe.id = generateId(); // Generate new IDs to avoid conflicts
                        });
                        
                        recipes = [...recipes, ...importedRecipes];
                        saveRecipes();
                        renderRecipeList();
                        
                        if (importedRecipes.length > 0) {
                            selectRecipe(importedRecipes[0].id);
                        }
                    }
                } catch (error) {
                    alert('Error importing recipes. Please check the file format.');
                }
            };
            reader.readAsText(file);
            
            // Reset the input
            event.target.value = '';
        }
    </script>
</body>
</html>'''

    def get_idea_capture_template(self):
        """Basic Idea Capture template"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Idea Capture NodePad</title>
</head>
<body>
    <div id="app">
        <h1>🧠 Idea Capture NodePad</h1>
        <p>Lightning-fast brain dump with auto-categorization</p>
        <!-- Template implementation would go here -->
    </div>
</body>
</html>'''

    def get_budget_manager_template(self):
        """Basic Budget Manager template"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Budget Manager NodePad</title>
</head>
<body>
    <div id="app">
        <h1>💰 Budget Manager NodePad</h1>
        <p>Visual budget planning with CSV import</p>
        <!-- Template implementation would go here -->
    </div>
</body>
</html>'''

    def get_basic_nodepad_template(self):
        """Basic NodePad 4.0.0 template"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NodePad</title>
</head>
<body>
    <div id="app">
        <h1>📝 NodePad 4.0.0</h1>
        <p>Clean NodePad starting point</p>
        <!-- Basic NodePad implementation would go here -->
    </div>
</body>
</html>'''

    def create_project_metadata(self, project_name, template_name, project_dir):
        """Create project metadata file"""
        metadata = {
            "name": project_name,
            "template": template_name,
            "created": datetime.now().isoformat(),
            "garden_version": "2.2",
            "deploy_manager_version": "2.2"
        }
        
        metadata_path = os.path.join(project_dir, '.garden-project.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def fork_garden_project(self):
        """Create a new project by forking GARDEN repository"""
        # Get project details
        project_name = input("📝 Project name: ").strip()
        if not project_name:
            print("❌ Project name required")
            return
        
        # Show available templates
        print("\n📋 Available templates:")
        template_keys = list(self.templates.keys())
        for i, template_name in enumerate(template_keys):
            template = self.templates[template_name]
            print(f"{i}. {template_name} - {template['description']}")
        
        try:
            template_idx = int(input(f"\n👉 Select template (0-{len(template_keys)-1}): "))
            template_name = template_keys[template_idx]
        except (ValueError, IndexError):
            print("❌ Invalid template selection")
            return
        
        print(f"\n🏗️ Creating project '{project_name}' with template '{template_name}'...")
        
        # Download GARDEN repository
        garden_source = self.download_garden_repo()
        if not garden_source:
            return
        
        try:
            # Create project directory
            project_dir = os.path.join(self.current_dir, project_name)
            if os.path.exists(project_dir):
                if not input(f"⚠️ Directory '{project_name}' exists. Overwrite? (y/N): ").lower().startswith('y'):
                    return
                shutil.rmtree(project_dir)
            
            os.makedirs(project_dir)
            
            # Copy core GARDEN files
            if not self.copy_core_files(garden_source, project_dir):
                print("❌ Failed to copy core files")
                return
            
            # Create template-specific files
            print("🎯 Creating starter application...")
            self.create_template_file(template_name, project_dir)
            
            # Initialize git repository
            os.chdir(project_dir)
            subprocess.run(['git', 'init'], capture_output=True)
            print("  ✓ Git repository initialized")
            
            # Create project metadata
            self.create_project_metadata(project_name, template_name, project_dir)
            print("  ✓ Project metadata created")
            
            os.chdir(self.current_dir)
            
            print(f"\n✅ Successfully forked garden project '{project_name}'!")
            print(f"📁 Location: {project_dir}")
            print("🌐 Ready for: Claude project knowledge upload")
            print("🚀 Deploy with: Option 1 (Deploy to Vercel)")
            
        finally:
            # Clean up temporary directory
            if 'garden_source' in locals():
                shutil.rmtree(os.path.dirname(garden_source), ignore_errors=True)

    def deploy_to_vercel(self):
        """Deploy existing project to Vercel"""
        print("🚀 Deploying to Vercel...")
        
        # Check if we're in a project directory
        if not os.path.exists('.garden-project.json'):
            print("❌ Not in a GARDEN project directory")
            print("   Run this from a project created with 'Fork New Garden Project'")
            return
        
        # Load project metadata
        with open('.garden-project.json', 'r') as f:
            metadata = json.load(f)
        
        project_name = metadata['name']
        
        # Check if Vercel CLI is available
        try:
            result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
            print(f"✅ Vercel CLI found: {result.stdout.strip()}")
        except FileNotFoundError:
            print("❌ Vercel CLI not found. Install with: npm i -g vercel")
            return
        
        # Deploy to Vercel
        print(f"🚀 Deploying '{project_name}' to Vercel...")
        try:
            deploy_result = subprocess.run(['vercel', '--prod'], capture_output=True, text=True)
            
            if deploy_result.returncode == 0:
                print("✅ Successfully deployed to Vercel!")
                print(f"🌐 URL: {deploy_result.stdout.strip()}")
            else:
                print(f"❌ Deployment failed: {deploy_result.stderr}")
                
        except Exception as e:
            print(f"❌ Deployment error: {str(e)}")

    def show_templates(self):
        """Show available project templates"""
        print("\n📋 Available Project Templates:")
        print("="*50)
        
        for name, template in self.templates.items():
            print(f"\n🎯 {name}")
            print(f"   Description: {template['description']}")
            print(f"   Main File: {template['main_file']}")
            print(f"   Type: {template['template_type']}")
            if template['contexts']:
                print(f"   Contexts: {', '.join(template['contexts'])}")

    def show_core_files(self):
        """Show core GARDEN files that get forked"""
        print("\n🧬 Core GARDEN DNA Files:")
        print("="*50)
        
        for core_file in self.core_files:
            if core_file.endswith('/'):
                print(f"📁 {core_file} (entire directory)")
            else:
                print(f"📄 {core_file}")
        
        print(f"\n📊 Total: {len(self.core_files)} core files/directories")

    def run(self):
        """Main application loop"""
        while True:
            self.show_banner()
            choice = self.show_menu()
            
            if choice == '0':
                self.fork_garden_project()
            elif choice == '1':
                self.deploy_to_vercel()
            elif choice == '2':
                self.test_github_connection()
            elif choice == '3':
                self.show_templates()
            elif choice == '4':
                self.show_core_files()
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option")
            
            if choice != '5':
                input("\n📱 Press Enter to continue...")

if __name__ == "__main__":
    manager = GardenDeployManager()
    manager.run()
