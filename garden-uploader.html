#!/usr/bin/env python3
"""
G.A.R.D.E.N. Deploy Manager v2.0 - Garden Fork System
Enhanced with repository forking and core file management
"""

import os
import sys
import json
import shutil
import subprocess
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
        self.garden_root = self.current_dir
        self.main_garden_url = "https://github.com/scottloeb/garden"
        
        # Core files that get forked to every project
        self.core_files = {
            'contexts/behindTheScenes/CIT_Brand_Style_Guide_20250511.md',
            'contexts/behindTheScenes/CIT_ADAcompliance_20250510.md',
            'contexts/behindTheScenes/CIT_Version_Control_20250511.md', 
            'contexts/behindTheScenes/CIT_meta-cit-framework_20250519.md',
            'contexts/CIT_Personal_20250518.md',
            'contexts/CIT_GARDEN_20250518.md',
            'toolshed/nodepad-4.0.0.html',
            '.gitignore'
        }
        
        # Project templates with their specific additional contexts
        self.project_templates = {
            'recipe': {
                'name': 'Recipe NodePad',
                'description': 'Recipe management with NodePad architecture',
                'additional_contexts': ['contexts/CIT_Cooking_*.md'],
                'starter_files': ['recipe-nodepad.html']
            },
            'budget': {
                'name': 'Budget NodePad', 
                'description': 'Financial management with graph visualization',
                'additional_contexts': ['contexts/CIT_BudgetNodePad_*.md'],
                'starter_files': ['budget-nodepad.html']
            },
            'sailing': {
                'name': 'Sailing Tools',
                'description': 'Marine navigation and planning tools',
                'additional_contexts': ['contexts/CIT_SailingWatch_*.md'],
                'starter_files': ['sailing-tools.html']
            },
            'planning': {
                'name': 'Planning NodePad',
                'description': 'Project and activity planning interface',
                'additional_contexts': ['contexts/CIT_Zach_*.md'],
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
        print("🌱 G.A.R.D.E.N. Deploy Manager v2.0 - Garden Fork System")
        print("=" * 60)
        print(f"{Colors.ENDC}")

    def print_menu(self):
        print(f"\n{Colors.OKBLUE}Available Operations:{Colors.ENDC}")
        print("0. 🌱 Fork New Garden Project (with core files)")
        print("1. 📂 List Existing Projects")
        print("2. 🚀 Deploy Project to Vercel")
        print("3. 📊 Project Status Dashboard") 
        print("4. 💾 Backup All Projects")
        print("5. 📤 Export Project")
        print("6. 🔄 Sync Core Files from Main Garden")
        print("7. 📋 Create Pull Request for Core Updates")
        print("8. 🧹 Clean Up Temporary Files")
        print("9. ❓ Help & Documentation")
        print("10. 🔧 System Status & Tool Check")
        print("q. Exit")

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
            self._fork_core_files(project_dir)
            
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
            print(f"{Colors.OKCYAN}🌐 Ready for: Claude project knowledge upload{Colors.ENDC}")
            print(f"{Colors.OKCYAN}🚀 Deploy with: Option 2 (Deploy to Vercel){Colors.ENDC}")
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error creating project: {str(e)}{Colors.ENDC}")
            if project_dir.exists():
                shutil.rmtree(project_dir)

    def _fork_core_files(self, project_dir):
        """Copy core GARDEN files to new project"""
        print(f"{Colors.OKCYAN}📋 Forking core GARDEN files...{Colors.ENDC}")
        
        for core_file in self.core_files:
            source_path = self.garden_root / core_file
            dest_path = project_dir / core_file
            
            if source_path.exists():
                # Create directory if needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, dest_path)
                print(f"  ✓ {core_file}")
            else:
                print(f"  ⚠️ Core file not found: {core_file}")

    def _add_template_contexts(self, project_dir, template):
        """Add template-specific context files"""
        if not template['additional_contexts']:
            return
            
        print(f"{Colors.OKCYAN}📋 Adding template-specific contexts...{Colors.ENDC}")
        
        for context_pattern in template['additional_contexts']:
            # Find matching context files
            import glob
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
        
        # Base content on Dan's NodePad pattern but recipe-focused
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
     */
    
    // Recipe-specific node types and emoji progression
    const RECIPE_EMOJIS = {
        recipe: '🍳',
        ingredient: '🥕', 
        step: '👨‍🍳',
        variation: '✨',
        note: '📝'
    };
    
    const RECIPE_PROGRESSION = {
        '🍳': '🥕',  // Recipe -> Ingredients
        '🥕': '👨‍🍳', // Ingredients -> Steps  
        '👨‍🍳': '✨',  // Steps -> Variations
        '✨': '📝'   // Variations -> Notes
    };
    
    // Initialize Recipe NodePad
    document.addEventListener('DOMContentLoaded', () => {
        // TODO: Implement recipe-specific NodePad
        // - Recipe cards with ingredients/steps hierarchy
        // - Print-friendly recipe cards (4x6)
        // - Shopping list generation
        // - Meal planning integration
        // - Nutrition tracking nodes
        
        document.getElementById('app').innerHTML = `
            <div style="padding: 2rem; text-align: center; font-family: system-ui;">
                <h1>🍳 Recipe NodePad</h1>
                <p>Recipe management with NodePad architecture</p>
                <p><em>Ready for implementation using Dan's NodePad 4.0.0 pattern</em></p>
                <div style="margin-top: 2rem; padding: 1rem; background: #f0f8ff; border-radius: 8px;">
                    <h3>Next Steps:</h3>
                    <ul style="text-align: left; display: inline-block;">
                        <li>Extend NodePad 4.0.0 with recipe-specific features</li>
                        <li>Add ingredient/step/variation node types</li>
                        <li>Implement 4x6 recipe card printing</li>
                        <li>Create shopping list generation</li>
                        <li>Add meal planning calendar</li>
                    </ul>
                </div>
            </div>
        `;
    });
    </script>
</body>
</html>'''
        
        recipe_html.write_text(recipe_content, encoding='utf-8')
        print(f"  ✓ recipe-nodepad.html (starter template)")

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
<html><head><title>Budget NodePad</title></head>
<body><h1>Budget NodePad - Ready for Implementation</h1></body></html>''')
            print(f"  ✓ budget-nodepad.html (placeholder)")

    def _create_sailing_tools(self, project_dir):
        """Create sailing-specific tools"""
        sailing_html = project_dir / "sailing-tools.html"
        sailing_html.write_text('''<!DOCTYPE html>
<html><head><title>Sailing Tools</title></head>
<body><h1>⛵ Sailing Tools - Ready for Implementation</h1></body></html>''')
        print(f"  ✓ sailing-tools.html (placeholder)")

    def _create_planning_nodepad(self, project_dir):
        """Create planning-specific NodePad"""
        planning_html = project_dir / "planning-nodepad.html"
        planning_html.write_text('''<!DOCTYPE html>
<html><head><title>Planning NodePad</title></head>
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
<html><head><title>NodePad</title></head>
<body><h1>NodePad - Ready for Implementation</h1></body></html>''')
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
            'garden_version': '2.0',
            'forked_from': 'scottloeb/garden',
            'core_files_synced': datetime.now().isoformat(),
            'deploy_status': 'not_deployed',
            'vercel_url': None
        }
        
        metadata_file = project_dir / ".garden-project.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        print(f"  ✓ Project metadata created")

    def sync_core_files(self):
        """Sync core files from main garden to all projects"""
        print(f"\n{Colors.HEADER}🔄 Sync Core Files from Main Garden{Colors.ENDC}")
        print("This will update core GARDEN files in all forked projects")
        
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return
            
        # Find all project directories
        project_dirs = [d for d in self.garden_root.iterdir() 
                       if d.is_dir() and (d / ".garden-project.json").exists()]
        
        if not project_dirs:
            print(f"{Colors.WARNING}⚠️ No forked projects found.{Colors.ENDC}")
            return
            
        print(f"Found {len(project_dirs)} forked projects:")
        for project_dir in project_dirs:
            print(f"  📁 {project_dir.name}")
            
        for project_dir in project_dirs:
            print(f"\n{Colors.OKCYAN}Updating {project_dir.name}...{Colors.ENDC}")
            self._fork_core_files(project_dir)
            
            # Update metadata
            metadata_file = project_dir / ".garden-project.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                metadata['core_files_synced'] = datetime.now().isoformat()
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                    
        print(f"\n{Colors.OKGREEN}✅ Core files synced to all projects!{Colors.ENDC}")

    def create_pull_request_helper(self):
        """Help create pull request for core updates"""
        print(f"\n{Colors.HEADER}📋 Create Pull Request for Core Updates{Colors.ENDC}")
        print("This will help you contribute improvements back to main GARDEN")
        
        # List projects with potential updates
        project_dirs = [d for d in self.garden_root.iterdir() 
                       if d.is_dir() and (d / ".garden-project.json").exists()]
        
        if not project_dirs:
            print(f"{Colors.WARNING}⚠️ No forked projects found.{Colors.ENDC}")
            return
            
        print(f"\nSelect project with updates to contribute:")
        for i, project_dir in enumerate(project_dirs):
            print(f"{i + 1}. {project_dir.name}")
            
        try:
            choice = int(input("Select project (number): ")) - 1
            if choice < 0 or choice >= len(project_dirs):
                raise ValueError()
            project_dir = project_dirs[choice]
        except (ValueError, IndexError):
            print(f"{Colors.FAIL}❌ Invalid selection.{Colors.ENDC}")
            return
            
        print(f"\n{Colors.OKCYAN}Analyzing {project_dir.name} for core file changes...{Colors.ENDC}")
        
        # Check for modified core files
        modified_files = []
        for core_file in self.core_files:
            project_file = project_dir / core_file
            main_file = self.garden_root / core_file
            
            if project_file.exists() and main_file.exists():
                # Simple file comparison (could be enhanced with git diff)
                project_content = project_file.read_text()
                main_content = main_file.read_text()
                
                if project_content != main_content:
                    modified_files.append(core_file)
                    
        if not modified_files:
            print(f"{Colors.WARNING}⚠️ No core file changes detected.{Colors.ENDC}")
            return
            
        print(f"\n{Colors.OKGREEN}Found {len(modified_files)} modified core files:{Colors.ENDC}")
        for file in modified_files:
            print(f"  📝 {file}")
            
        print(f"\n{Colors.OKCYAN}Next steps:{Colors.ENDC}")
        print("1. Review changes in each file")
        print("2. Create feature branch in main GARDEN repo")
        print("3. Copy updated files to main repo")
        print("4. Commit changes with descriptive message")
        print("5. Push branch and create pull request")
        print(f"\n{Colors.WARNING}💡 Consider creating a script to automate this process!{Colors.ENDC}")

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
                    print("\n📂 List Existing Projects - TODO: Implement")
                elif choice == '2':
                    print("\n🚀 Deploy Project to Vercel - TODO: Implement")
                elif choice == '3':
                    print("\n📊 Project Status Dashboard - TODO: Implement")
                elif choice == '4':
                    print("\n💾 Backup All Projects - TODO: Implement")
                elif choice == '5':
                    print("\n📤 Export Project - TODO: Implement")
                elif choice == '6':
                    self.sync_core_files()
                elif choice == '7':
                    self.create_pull_request_helper()
                elif choice == '8':
                    print("\n🧹 Clean Up Temporary Files - TODO: Implement")
                elif choice == '9':
                    print("\n❓ Help & Documentation - TODO: Implement")
                elif choice == '10':
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
