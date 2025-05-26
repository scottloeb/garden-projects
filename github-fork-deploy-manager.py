#!/usr/bin/env python3
"""
G.A.R.D.E.N. TRUE GitHub Fork Deploy Manager v2.3
Downloads core files directly from GitHub repository
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime
import urllib.request

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class GitHubForkManager:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.github_repo = "scottloeb/garden"
        self.github_zip_url = f"https://github.com/{self.github_repo}/archive/refs/heads/main.zip"
        
        # Core files to extract from GitHub
        self.core_files = [
            'contexts/',
            'toolshed/nodepad-4.0.0.html',
            'generated/',
            'module-generators/',
            'sunflower/',
            'CONTRIBUTING.md',
            'README.md',
            'requirements.txt',
            '.gitignore'
        ]
        
        self.project_templates = {
            'recipe': {
                'name': 'Recipe NodePad',
                'description': 'Recipe management with hierarchical ingredients and 4x6 printing',
                'starter_app': 'recipe-nodepad.html'
            },
            'budget': {
                'name': 'Budget NodePad',
                'description': 'Financial planning with Grassroots structure',
                'starter_app': 'budget-nodepad.html'
            },
            'planning': {
                'name': 'Planning NodePad',
                'description': 'PDA-friendly project planning',
                'starter_app': 'planning-nodepad.html'
            },
            'sailing': {
                'name': 'Sailing Tools',
                'description': 'Marine navigation with Apple Watch integration',
                'starter_app': 'sailing-tools.html'
            },
            'nodepad': {
                'name': 'Pure NodePad',
                'description': 'Clean NodePad for any domain',
                'starter_app': 'nodepad.html'
            }
        }

    def test_github_connection(self):
        """Test connection to GitHub repository"""
        print(f"\n{Colors.HEADER}🔍 Testing GitHub Connection{Colors.ENDC}")
        print(f"Repository: {self.github_repo}")
        print(f"URL: {self.github_zip_url}")
        
        try:
            print("Connecting to GitHub...")
            with urllib.request.urlopen(self.github_zip_url) as response:
                size = len(response.read())
                print(f"{Colors.OKGREEN}✅ Connection successful!{Colors.ENDC}")
                print(f"Repository size: {size:,} bytes")
                return True
        except Exception as e:
            print(f"{Colors.FAIL}❌ Connection failed: {str(e)}{Colors.ENDC}")
            return False

    def download_garden_repo(self):
        """Download the latest GARDEN repository from GitHub"""
        print(f"\n{Colors.OKCYAN}📥 Downloading latest GARDEN repository...{Colors.ENDC}")
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="garden_download_")
        zip_path = Path(temp_dir) / "garden.zip"
        extract_path = Path(temp_dir) / "extracted"
        
        try:
            # Download repository zip
            print("Downloading repository...")
            urllib.request.urlretrieve(self.github_zip_url, zip_path)
            print(f"✓ Downloaded to {zip_path}")
            
            # Extract zip
            print("Extracting repository...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            # Find the extracted garden directory (usually garden-main/)
            extracted_dirs = list(extract_path.glob("garden-*"))
            if not extracted_dirs:
                raise Exception("Could not find extracted garden directory")
            
            garden_dir = extracted_dirs[0]
            print(f"✓ Extracted to {garden_dir}")
            
            return garden_dir
            
        except Exception as e:
            # Cleanup on error
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise Exception(f"Download failed: {str(e)}")

    def fork_garden_project(self):
        """Create a new project by forking from GitHub"""
        print(f"\n{Colors.HEADER}🌱 Fork Garden Project from GitHub{Colors.ENDC}")
        
        # Project name
        project_name = input("Enter project name: ").strip()
        if not project_name:
            print(f"{Colors.FAIL}❌ Project name required{Colors.ENDC}")
            return
        
        # Template selection
        print(f"\n{Colors.OKBLUE}Select Template:{Colors.ENDC}")
        templates = list(self.project_templates.items())
        for i, (key, template) in enumerate(templates):
            print(f"{i + 1}. {template['name']} - {template['description']}")
        
        try:
            choice = int(input("Select template: ")) - 1
            template_key, template = templates[choice]
        except (ValueError, IndexError):
            print(f"{Colors.FAIL}❌ Invalid selection{Colors.ENDC}")
            return
        
        print(f"\n{Colors.WARNING}🚀 Creating {project_name} with {template['name']}...{Colors.ENDC}")
        
        # Check if project exists
        project_dir = self.current_dir / project_name
        if project_dir.exists():
            print(f"{Colors.FAIL}❌ Project already exists: {project_dir}{Colors.ENDC}")
            return
        
        try:
            # Download latest GARDEN
            garden_dir = self.download_garden_repo()
            
            # Create project directory
            project_dir.mkdir()
            print(f"✓ Created project directory: {project_dir}")
            
            # Copy core files
            copied_count = self._copy_core_files(garden_dir, project_dir)
            
            # Create starter app
            self._create_starter_app(project_dir, template_key, template)
            
            # Initialize git
            self._init_git(project_dir, project_name)
            
            # Create metadata
            self._create_metadata(project_dir, project_name, template_key)
            
            # Cleanup
            shutil.rmtree(garden_dir.parent.parent, ignore_errors=True)
            
            print(f"\n{Colors.OKGREEN}✅ Successfully forked {project_name}!{Colors.ENDC}")
            print(f"{Colors.OKCYAN}📁 Location: {project_dir}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}📄 Core files: {copied_count}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}🌐 Ready for Claude project knowledge upload{Colors.ENDC}")
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Fork failed: {str(e)}{Colors.ENDC}")
            if project_dir.exists():
                shutil.rmtree(project_dir, ignore_errors=True)

    def _copy_core_files(self, garden_dir, project_dir):
        """Copy core files from downloaded garden repo"""
        print(f"{Colors.OKCYAN}📋 Copying core GARDEN files...{Colors.ENDC}")
        
        copied_count = 0
        
        for core_pattern in self.core_files:
            source_path = garden_dir / core_pattern.rstrip('/')
            dest_path = project_dir / core_pattern.rstrip('/')
            
            if source_path.exists():
                if source_path.is_file():
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, dest_path)
                    print(f"  ✓ {core_pattern}")
                    copied_count += 1
                elif source_path.is_dir():
                    shutil.copytree(source_path, dest_path)
                    file_count = len(list(dest_path.rglob('*')))
                    print(f"  ✓ {core_pattern} ({file_count} files)")
                    copied_count += file_count
            else:
                print(f"  ⚠️ Not found: {core_pattern}")
        
        return copied_count

    def _create_starter_app(self, project_dir, template_key, template):
        """Create template-specific starter application"""
        print(f"{Colors.OKCYAN}🎯 Creating {template['name']}...{Colors.ENDC}")
        
        app_file = project_dir / template['starter_app']
        
        if template_key == 'recipe':
            app_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Recipe NodePad - GARDEN Fork</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div id="app">
        <div style="padding: 2rem; text-align: center; font-family: system-ui;">
            <h1>🍳 Recipe NodePad - GitHub Fork Ready!</h1>
            <p>Complete recipe management forked from GARDEN repository</p>
            <div style="margin-top: 2rem; padding: 1rem; background: #f0f8ff; border-radius: 8px;">
                <h3>✅ Project Ready for Development:</h3>
                <ul style="text-align: left; display: inline-block;">
                    <li>📁 Complete GARDEN core files downloaded from GitHub</li>
                    <li>🧬 All cognitive frameworks included</li>
                    <li>🛠️ NodePad 4.0.0 pattern ready</li>
                    <li>⚙️ Module generators for database integration</li>
                    <li>🌻 Sunflower pattern engine</li>
                    <li>🎨 Brand standards and accessibility guidelines</li>
                </ul>
            </div>
            <p style="margin-top: 2rem; color: #666;">
                <strong>Next:</strong> Upload entire project folder to Claude project knowledge and begin development!
            </p>
        </div>
    </div>
</body>
</html>'''
        else:
            app_content = f'''<!DOCTYPE html>
<html><head><title>{template["name"]} - GARDEN Fork</title></head>
<body><h1>{template["name"]} - Ready for Implementation</h1></body></html>'''
        
        app_file.write_text(app_content, encoding='utf-8')
        print(f"  ✓ {template['starter_app']}")

    def _init_git(self, project_dir, project_name):
        """Initialize git repository"""
        try:
            subprocess.run(['git', 'init'], cwd=project_dir, check=True, capture_output=True)
            subprocess.run(['git', 'add', '.'], cwd=project_dir, check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', f'Initial commit: {project_name} forked from GARDEN'], 
                         cwd=project_dir, check=True, capture_output=True)
            print(f"  ✓ Git repository initialized")
        except:
            print(f"  ⚠️ Git initialization failed")

    def _create_metadata(self, project_dir, project_name, template_key):
        """Create project metadata"""
        metadata = {
            'name': project_name,
            'template': template_key,
            'created': datetime.now().isoformat(),
            'forked_from': self.github_repo,
            'garden_version': '2.3',
            'github_fork': True
        }
        
        (project_dir / ".garden-project.json").write_text(json.dumps(metadata, indent=2))
        print(f"  ✓ Project metadata created")

    def run(self):
        """Main menu"""
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("🌱 G.A.R.D.E.N. GitHub Fork System v2.3")
        print("=" * 50)
        print(f"{Colors.ENDC}")
        
        while True:
            print(f"\n{Colors.OKBLUE}Options:{Colors.ENDC}")
            print("0. 🌱 Fork New Project from GitHub")
            print("1. 🔍 Test GitHub Connection")
            print("q. Exit")
            
            choice = input(f"\n{Colors.OKBLUE}Choice: {Colors.ENDC}").strip().lower()
            
            if choice == 'q':
                print("🌱 Happy gardening!")
                break
            elif choice == '0':
                self.fork_garden_project()
            elif choice == '1':
                self.test_github_connection()
            else:
                print(f"{Colors.FAIL}❌ Invalid choice{Colors.ENDC}")

if __name__ == "__main__":
    manager = GitHubForkManager()
    manager.run()