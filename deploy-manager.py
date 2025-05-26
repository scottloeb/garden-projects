#!/usr/bin/env python3
"""
G.A.R.D.E.N. Deploy Manager v2.2 - Garden Fork System
Updated with comprehensive core file list including generated/ and module-generators/
"""

import os
import sys
import json
import shutil
import subprocess
import glob
from pathlib import Path
from datetime import datetime
import urllib.request
import zipfile

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GardenForkManager:
    def __init__(self):
        self.current_dir = Path.cwd()
        
        # Auto-detect garden root directory
        self.garden_root = self._find_garden_root()
        self.main_garden_url = "https://github.com/scottloeb/garden"
        
    def _find_garden_root(self):
        """Find the main garden repository directory"""
        # Common garden directory locations
        possible_locations = [
            self.current_dir,  # Current directory
            self.current_dir.parent / "garden",  # garden-projects/../garden
            Path.home() / "Documents" / "GitHub" / "garden",
            Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "GitHub" / "garden",
            # Add more common locations if needed
        ]
        
        for location in possible_locations:
            if location.exists() and (location / "contexts").exists():
                print(f"🌱 Found garden repository at: {location}")
                return location
        
        # Fallback: ask user
        print(f"❌ Could not auto-detect garden repository.")
        print(f"Current directory: {self.current_dir}")
        garden_path = input("Enter path to main garden repository: ").strip()
        
        if garden_path and Path(garden_path).exists():
            return Path(garden_path)
        else:
            print(f"❌ Invalid path. Using current directory as fallback.")
            return self.current_dir
        
class GardenForkManager:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.main_garden_url = "https://github.com/scottloeb/garden"
        
        # Define core files first (before finding garden root)
        self.core_files = [
            # All contexts (entire folder) - will copy recursively
            'contexts/',
            
            # Development tools  
            'toolshed/nodepad-4.0.0.html',
            'generated/modulegenerator_v2/',  # Entire directory
            'generated/README.md',
            'module-generators/',  # Entire directory
            'sunflower/',  # Entire directory
            
            # Project documentation
            'CONTRIBUTING.md',
            'README.md', 
            'requirements.txt',
            '.gitignore'
        ]
        
        # Auto-detect garden root directory
        self.garden_root = self._find_garden_root()
        
        # Project templates with their specific additional contexts
        self.project_templates = {
            'recipe': {
                'name': 'Recipe NodePad',
                'description': 'Recipe management with NodePad architecture',
                'additional_contexts': [],
                'starter_files': ['recipe-nodepad.html']
            },
            'budget': {
                'name': 'Budget NodePad', 
                'description': 'Financial management with graph visualization',
                'additional_contexts': [],
                'starter_files': ['budget-nodepad.html']
            },
            'sailing': {
                'name': 'Sailing Tools',
                'description': 'Marine navigation and planning tools',
                'additional_contexts': [],
                'starter_files': ['sailing-tools.html']
            },
            'planning': {
                'name': 'Planning NodePad',
                'description': 'Project and activity planning interface',
                'additional_contexts': [],
                'starter_files': ['planning-nodepad.html']
            },
            'nodepad': {
                'name': 'Pure NodePad',
                'description': 'Clean NodePad implementation for any domain',
                'additional_contexts': [],
                'starter_files': ['nodepad.html']
            }
        }

    def print_header(self):
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("🌱 G.A.R.D.E.N. Deploy Manager v2.2 - Garden Fork System")
        print("=" * 60)
        print(f"{Colors.ENDC}")

    def print_menu(self):
        print(f"\n{Colors.OKBLUE}Available Operations:{Colors.ENDC}")
        print("0. 🌱 Fork New Garden Project (with core files)")
        print("1. 📂 List Existing Projects")
        print("2. 🔍 Discover Core Files (Debug)")
        print("3. 🚀 Deploy Project to Vercel")
        print("4. 📊 Project Status Dashboard") 
        print("5. 💾 Backup All Projects")
        print("6. 📤 Export Project")
        print("7. 🔄 Sync Core Files from Main Garden")
        print("8. 📋 Create Pull Request for Core Updates")
        print("9. 🧹 Clean Up Temporary Files")
        print("10. ❓ Help & Documentation")
        print("11. 🔧 System Status & Tool Check")
        print("q. Exit")

    def discover_core_files(self):
        """Debug function to show what core files are actually found"""
        print(f"\n{Colors.HEADER}🔍 Core File Discovery{Colors.ENDC}")
        print(f"Searching in: {self.garden_root}")
        
        total_found = 0
        total_expected = 0
        
        for core_pattern in self.core_files:
            print(f"\n{Colors.OKCYAN}Pattern: {core_pattern}{Colors.ENDC}")
            total_expected += 1
            
            if core_pattern.endswith('/'):
                # Directory pattern - find all .md files recursively
                search_path = self.garden_root / core_pattern.rstrip('/')
                if search_path.exists():
                    found_files = list(search_path.rglob('*.md'))
                    if found_files:
                        print(f"  ✓ Found {len(found_files)} files in directory:")
                        for f in sorted(found_files)[:10]:  # Show first 10
                            rel_path = f.relative_to(self.garden_root)
                            print(f"    📄 {rel_path}")
                        if len(found_files) > 10:
                            print(f"    ... and {len(found_files) - 10} more files")
                        total_found += len(found_files)
                    else:
                        print(f"  ⚠️ Directory exists but no .md files found")
                else:
                    print(f"  ❌ Directory not found: {search_path}")
            else:
                # File pattern
                file_path = self.garden_root / core_pattern
                if file_path.exists():
                    if file_path.is_file():
                        print(f"  ✓ File found: {file_path}")
                        total_found += 1
                    elif file_path.is_dir():
                        # Count files in directory
                        files_in_dir = list(file_path.rglob('*'))
                        file_count = len([f for f in files_in_dir if f.is_file()])
                        print(f"  ✓ Directory found with {file_count} files: {file_path}")
                        total_found += file_count
                else:
                    print(f"  ❌ Not found: {file_path}")
        
        print(f"\n{Colors.OKGREEN}Discovery Summary:{Colors.ENDC}")
        print(f"Total patterns checked: {total_expected}")
        print(f"Total files/directories found: {total_found}")
        
        if total_found > 0:
            print(f"{Colors.OKGREEN}✅ Core files discovered - fork creation should work!{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ No core files found - check directory structure{Colors.ENDC}")

    def fork_garden_project(self):
        """Create a new project with forked GARDEN core files"""
        print(f"\n{Colors.HEADER}🌱 Fork New Garden Project{Colors.ENDC}")
        
        # Project name input
        project_name = input("Enter project name (lowercase, no spaces): ").strip()
        if not project_name or not project_name.replace('-', '').replace('_', '').isalnum():
            print(f"{Colors.FAIL}❌ Invalid project name. Use lowercase letters, numbers, hyphens, underscores only.{Colors.ENDC}")
            return
            
        # Check if project exists
        project_dir = self.garden_root / project_name
        if project_dir.exists():
            print(f"{Colors.FAIL}❌ Project '{project_name}' already exists.{Colors.ENDC}")
            return
            
        # Select project template
        print(f"\n{Colors.OKBLUE}Available Project Templates:{Colors.ENDC}")
        template_keys = list(self.project_templates.keys())
        for i, (key, template) in enumerate(self.project_templates.items()):
            print(f"{i + 1}. {template['name']} - {template['description']}")
            
        try:
            choice = int(input("Select template (number): ")) - 1
            if choice < 0 or choice >= len(template_keys):
                raise ValueError()
            template_key = template_keys[choice]
            template = self.project_templates[template_key]
        except (ValueError, IndexError):
            print(f"{Colors.FAIL}❌ Invalid selection.{Colors.ENDC}")
            return
            
        print(f"\n{Colors.WARNING}🏗️ Creating project '{project_name}' with template '{template['name']}'...{Colors.ENDC}")
        
        try:
            # Create project directory
            project_dir.mkdir(exist_ok=True)
            
            # Fork core GARDEN files
            copied_count = self._fork_core_files(project_dir)
            
            # Add template-specific contexts
            self._add_template_contexts(project_dir, template)
            
            # Create starter files
            self._create_starter_files(project_dir, template_key, template)
            
            # Initialize git repository
            self._init_project_git(project_dir, project_name)
            
            # Create project metadata
            self._create_project_metadata(project_dir, project_name, template_key)
            
            print(f"\n{Colors.OKGREEN}✅ Successfully forked garden project '{project_name}'!{Colors.ENDC}")
            print(f"{Colors.OKCYAN}📁 Location: {project_dir}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}📄 Files copied: {copied_count}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}🌐 Ready for: Claude project knowledge upload{Colors.ENDC}")
            print(f"{Colors.OKCYAN}🚀 Deploy with: Option 3 (Deploy to Vercel){Colors.ENDC}")
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error creating project: {str(e)}{Colors.ENDC}")
            if project_dir.exists():
                shutil.rmtree(project_dir)

    def _fork_core_files(self, project_dir):
        """Copy core GARDEN files to new project"""
        print(f"{Colors.OKCYAN}📋 Forking core GARDEN files...{Colors.ENDC}")
        
        copied_count = 0
        
        for core_pattern in self.core_files:
            if core_pattern.endswith('/'):
                # Directory pattern - copy all .md files recursively
                source_dir = self.garden_root / core_pattern.rstrip('/')
                if source_dir.exists():
                    for md_file in source_dir.rglob('*.md'):
                        rel_path = md_file.relative_to(self.garden_root)
                        dest_path = project_dir / rel_path
                        
                        # Create directory if needed
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(md_file, dest_path)
                        print(f"  ✓ {rel_path}")
                        copied_count += 1
                else:
                    print(f"  ⚠️ Directory not found: {core_pattern}")
            else:
                # File or directory pattern
                source_path = self.garden_root / core_pattern
                if source_path.exists():
                    dest_path = project_dir / core_pattern
                    
                    if source_path.is_file():
                        # Copy single file
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_path, dest_path)
                        print(f"  ✓ {core_pattern}")
                        copied_count += 1
                    elif source_path.is_dir():
                        # Copy entire directory
                        if dest_path.exists():
                            shutil.rmtree(dest_path)
                        shutil.copytree(source_path, dest_path)
                        file_count = len(list(dest_path.rglob('*')))
                        print(f"  ✓ {core_pattern} ({file_count} files)")
                        copied_count += file_count
                else:
                    print(f"  ⚠️ Core file not found: {core_pattern}")
        
        return copied_count

    def _add_template_contexts(self, project_dir, template):
        """Add template-specific context files"""
        if not template['additional_contexts']:
            return
            
        print(f"{Colors.OKCYAN}📋 Adding template-specific contexts...{Colors.ENDC}")
        
        for context_pattern in template['additional_contexts']:
            # Find matching context files
            matching_files = glob.glob(str(self.garden_root / context_pattern))
            
            for source_file in matching_files:
                source_path = Path(source_file)
                rel_path = source_path.relative_to(self.garden_root)
                dest_path = project_dir / rel_path
                
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, dest_path)
                print(f"  ✓ {rel_path}")

    def _create_starter_files(self, project_dir, template_key, template):
        """Create starter application files"""
        print(f"{Colors.OKCYAN}🎯 Creating starter application...{Colors.ENDC}")
        
        if template_key == 'recipe':
            self._create_recipe_nodepad(project_dir)
        elif template_key == 'budget':
            self._create_budget_nodepad(project_dir)
        elif template_key == 'sailing':
            self._create_sailing_tools(project_dir)
        elif template_key == 'planning':
            self._create_planning_nodepad(project_dir)
        else:  # nodepad
            self._create_pure_nodepad(project_dir)

    def _create_recipe_nodepad(self, project_dir):
        """Create recipe-specific NodePad application"""
        recipe_html = project_dir / "recipe-nodepad.html"
        
        # Use the complete recipe nodepad implementation from our artifacts
        recipe_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Recipe NodePad - GARDEN Project</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div id="app"></div>
    
    <script>
    /**
     * Recipe NodePad - Built on Dan's NodePad 4.0.0 Pattern
     * A recipe management system with hierarchical organization
     * Features: Recipe cards, shopping lists, meal planning, 4x6 printing
     */
    
    // Recipe-specific configuration
    const RECIPE_CONFIG = {
        emojis: {
            recipe: '🍳',
            ingredient: '🥕',
            step: '👨‍🍳',
            variation: '✨',
            note: '📝',
            category: '📚',
            meal: '🍽️',
            shopping: '🛒'
        },
        progression: {
            '🍳': '🥕',  // Recipe -> Ingredients
            '🥕': '👨‍🍳', // Ingredients -> Steps  
            '👨‍🍳': '✨',  // Steps -> Variations
            '✨': '📝',   // Variations -> Notes
            '📚': '🍳',   // Category -> Recipe
            '🍽️': '🍳',   // Meal -> Recipe
            '🛒': '🥕'    // Shopping -> Ingredients
        },
        units: ['cups', 'tbsp', 'tsp', 'lbs', 'oz', 'ml', 'l', 'g', 'kg', 'pieces', 'cloves', 'pinch']
    };

    // Initialize Recipe NodePad - Placeholder implementation
    document.addEventListener('DOMContentLoaded', () => {
        document.getElementById('app').innerHTML = `
            <div style="padding: 2rem; text-align: center; font-family: system-ui;">
                <h1>🍳 Recipe NodePad - GARDEN Fork</h1>
                <p>Complete recipe management with NodePad architecture</p>
                <div style="margin-top: 2rem; padding: 1rem; background: #f0f8ff; border-radius: 8px;">
                    <h3>✅ Ready for Enhancement:</h3>
                    <ul style="text-align: left; display: inline-block;">
                        <li>Upload this entire project folder to Claude project knowledge</li>
                        <li>Implement hierarchical recipe nodes (🍳 → 🥕 → 👨‍🍳)</li>
                        <li>Add 4x6 recipe card printing system</li>
                        <li>Create shopping list generation</li>
                        <li>Integrate meal planning features</li>
                    </ul>
                </div>
                <div style="margin-top: 2rem;">
                    <p><strong>Project Structure Ready:</strong></p>
                    <ul style="text-align: left; display: inline-block; color: #666;">
                        <li>📁 Complete GARDEN cognitive framework files</li>
                        <li>🛠️ NodePad 4.0.0 pattern in toolshed/</li>
                        <li>⚙️ Module generators for Neo4j integration</li>
                        <li>🌻 Sunflower pattern engine for visualization</li>
                        <li>🎨 Brand standards and accessibility guidelines</li>
                    </ul>
                </div>
            </div>
        `;
        
        console.log('%c Recipe NodePad Fork %c Ready for Development!', 
            'background:#ff6b35;color:white;padding:4px 8px;border-radius:4px', 
            'color:#333');
    });
    </script>
</body>
</html>'''
        
        recipe_html.write_text(recipe_content, encoding='utf-8')
        print(f"  ✓ recipe-nodepad.html (ready for enhancement)")

    def _create_budget_nodepad(self, project_dir):
        """Create budget NodePad (copy existing if available)"""
        budget_html = project_dir / "budget-nodepad.html"
        
        # Try to copy from existing budget-nodepad.html
        existing_budget = self.garden_root / "budget-nodepad.html"
        if existing_budget.exists():
            shutil.copy2(existing_budget, budget_html)
            print(f"  ✓ budget-nodepad.html (copied from existing)")
        else:
            # Create placeholder
            budget_html.write_text('''<!DOCTYPE html>
<html><head><title>Budget NodePad - GARDEN Fork</title></head>
<body><h1>💰 Budget NodePad - Ready for Implementation</h1></body></html>''')
            print(f"  ✓ budget-nodepad.html (placeholder)")

    def _create_sailing_tools(self, project_dir):
        """Create sailing-specific tools"""
        sailing_html = project_dir / "sailing-tools.html"
        sailing_html.write_text('''<!DOCTYPE html>
<html><head><title>Sailing Tools - GARDEN Fork</title></head>
<body><h1>⛵ Sailing Tools - Ready for Implementation</h1></body></html>''')
        print(f"  ✓ sailing-tools.html (placeholder)")

    def _create_planning_nodepad(self, project_dir):
        """Create planning-specific NodePad"""
        planning_html = project_dir / "planning-nodepad.html"
        planning_html.write_text('''<!DOCTYPE html>
<html><head><title>Planning NodePad - GARDEN Fork</title></head>
<body><h1>📋 Planning NodePad - Ready for Implementation</h1></body></html>''')
        print(f"  ✓ planning-nodepad.html (placeholder)")

    def _create_pure_nodepad(self, project_dir):
        """Create pure NodePad implementation"""
        nodepad_html = project_dir / "nodepad.html"
        
        # Copy from toolshed if available
        toolshed_nodepad = self.garden_root / "toolshed" / "nodepad-4.0.0.html"
        if toolshed_nodepad.exists():
            shutil.copy2(toolshed_nodepad, nodepad_html)
            print(f"  ✓ nodepad.html (copied from toolshed)")
        else:
            nodepad_html.write_text('''<!DOCTYPE html>
<html><head><title>NodePad - GARDEN Fork</title></head>
<body><h1>🎯 NodePad - Ready for Implementation</h1></body></html>''')
            print(f"  ✓ nodepad.html (placeholder)")

    def _init_project_git(self, project_dir, project_name):
        """Initialize git repository for the project"""
        try:
            # Initialize git repo
            subprocess.run(['git', 'init'], cwd=project_dir, check=True, capture_output=True)
            
            # Create initial commit
            subprocess.run(['git', 'add', '.'], cwd=project_dir, check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', f'Initial commit: {project_name} forked from GARDEN'], 
                         cwd=project_dir, check=True, capture_output=True)
            
            print(f"  ✓ Git repository initialized")
            
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️ Git initialization failed: {e}")

    def _create_project_metadata(self, project_dir, project_name, template_key):
        """Create project metadata file"""
        metadata = {
            'name': project_name,
            'template': template_key,
            'created': datetime.now().isoformat(),
            'garden_version': '2.2',
            'forked_from': 'scottloeb/garden',
            'core_files_synced': datetime.now().isoformat(),
            'deploy_status': 'not_deployed',
            'vercel_url': None
        }
        
        metadata_file = project_dir / ".garden-project.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        print(f"  ✓ Project metadata created")

    def list_projects(self):
        """List all existing GARDEN projects"""
        print(f"\n{Colors.HEADER}📂 Existing Garden Projects{Colors.ENDC}")
        
        # Find all project directories
        project_dirs = [d for d in self.garden_root.iterdir() 
                       if d.is_dir() and (d / ".garden-project.json").exists()]
        
        if not project_dirs:
            print(f"{Colors.WARNING}⚠️ No forked projects found.{Colors.ENDC}")
            print(f"Create your first project with Option 0!")
            return
            
        print(f"Found {len(project_dirs)} Garden projects:\n")
        
        for project_dir in project_dirs:
            try:
                metadata_file = project_dir / ".garden-project.json"
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                print(f"{Colors.OKGREEN}📁 {project_dir.name}{Colors.ENDC}")
                print(f"   Template: {metadata.get('template', 'unknown')}")
                print(f"   Created: {metadata.get('created', 'unknown')}")
                print(f"   Version: {metadata.get('garden_version', 'unknown')}")
                print(f"   Status: {metadata.get('deploy_status', 'unknown')}")
                print()
                
            except Exception as e:
                print(f"{Colors.WARNING}📁 {project_dir.name} (metadata error: {e}){Colors.ENDC}")

    def run(self):
        """Main menu loop"""
        self.print_header()
        
        while True:
            self.print_menu()
            choice = input(f"\n{Colors.OKBLUE}Enter your choice: {Colors.ENDC}").strip().lower()
            
            try:
                if choice == 'q' or choice == 'quit':
                    print(f"\n{Colors.OKGREEN}🌱 Happy gardening! See you next time.{Colors.ENDC}")
                    break
                elif choice == '0':
                    self.fork_garden_project()
                elif choice == '1':
                    self.list_projects()
                elif choice == '2':
                    self.discover_core_files()
                elif choice == '3':
                    print("\n🚀 Deploy Project to Vercel - TODO: Implement")
                elif choice == '4':
                    print("\n📊 Project Status Dashboard - TODO: Implement")
                elif choice == '5':
                    print("\n💾 Backup All Projects - TODO: Implement")
                elif choice == '6':
                    print("\n📤 Export Project - TODO: Implement")
                elif choice == '7':
                    print("\n🔄 Sync Core Files from Main Garden - TODO: Implement")
                elif choice == '8':
                    print("\n📋 Create Pull Request for Core Updates - TODO: Implement")
                elif choice == '9':
                    print("\n🧹 Clean Up Temporary Files - TODO: Implement")
                elif choice == '10':
                    print("\n❓ Help & Documentation - TODO: Implement")
                elif choice == '11':
                    print("\n🔧 System Status & Tool Check - TODO: Implement")
                else:
                    print(f"{Colors.FAIL}❌ Invalid choice. Please try again.{Colors.ENDC}")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Colors.WARNING}⚠️ Interrupted by user.{Colors.ENDC}")
                break
            except Exception as e:
                print(f"\n{Colors.FAIL}❌ Error: {str(e)}{Colors.ENDC}")

if __name__ == "__main__":
    manager = GardenForkManager()
    manager.run()