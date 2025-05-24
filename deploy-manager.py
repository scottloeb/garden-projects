#!/usr/bin/env python3
"""
G.A.R.D.E.N. Deploy Manager - Complete Version with Menu Loop
Phase 1 Enhancement: Persistent menu system with full project management
"""

import os
import sys
import shutil
import json
import subprocess
from datetime import datetime
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class GARDENDeployManager:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.pending_dir = self.root_dir / "pending-updates"
        self.deployed_dir = self.root_dir / "deployed-projects"
        self.templates_dir = self.root_dir / "project-templates"
        
        # Ensure directories exist
        self.pending_dir.mkdir(exist_ok=True)
        self.deployed_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        
        print(f"{Colors.HEADER}🌱 G.A.R.D.E.N. Deploy Manager v1.1{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Location: {self.root_dir}{Colors.ENDC}")
        print()

    def show_menu(self):
        """Display the main menu"""
        print(f"{Colors.BOLD}═══════════════════════════════════════════════════════════════════{Colors.ENDC}")
        print(f"{Colors.HEADER}🌱 G.A.R.D.E.N. PROJECT MANAGEMENT MENU{Colors.ENDC}")
        print(f"{Colors.BOLD}═══════════════════════════════════════════════════════════════════{Colors.ENDC}")
        print()
        print(f"{Colors.OKGREEN}📋 PROJECT OPERATIONS:{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}1.{Colors.ENDC} List pending projects")
        print(f"  {Colors.OKCYAN}2.{Colors.ENDC} Create new project")
        print(f"  {Colors.OKCYAN}3.{Colors.ENDC} View project details")
        print(f"  {Colors.OKCYAN}4.{Colors.ENDC} Deploy project to Vercel")
        print()
        print(f"{Colors.OKGREEN}🔧 SYSTEM OPERATIONS:{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}5.{Colors.ENDC} Initialize Git repository")
        print(f"  {Colors.OKCYAN}6.{Colors.ENDC} Create web uploader interface")
        print(f"  {Colors.OKCYAN}7.{Colors.ENDC} System status")
        print()
        print(f"{Colors.OKGREEN}📊 DATA OPERATIONS:{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}8.{Colors.ENDC} Export project list")
        print(f"  {Colors.OKCYAN}9.{Colors.ENDC} Backup projects")
        print()
        print(f"  {Colors.WARNING}0.{Colors.ENDC} Exit")
        print(f"{Colors.BOLD}═══════════════════════════════════════════════════════════════════{Colors.ENDC}")
        print()

    def list_pending_projects(self):
        """List all projects in pending-updates directory"""
        print(f"{Colors.HEADER}📋 PENDING PROJECTS{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        
        if not self.pending_dir.exists():
            print(f"{Colors.WARNING}No pending-updates directory found.{Colors.ENDC}")
            return
        
        projects = [d for d in self.pending_dir.iterdir() if d.is_dir()]
        
        if not projects:
            print(f"{Colors.WARNING}No pending projects found.{Colors.ENDC}")
            print(f"Create a new project with option 2.")
            return
        
        for i, project in enumerate(projects, 1):
            print(f"{Colors.OKGREEN}{i:2d}.{Colors.ENDC} {project.name}")
            
            # Show project contents briefly
            files = list(project.iterdir())[:3]  # Show first 3 files
            for file in files:
                if file.is_file():
                    print(f"     📄 {file.name}")
                elif file.is_dir():
                    print(f"     📁 {file.name}/")
            
            if len(list(project.iterdir())) > 3:
                remaining = len(list(project.iterdir())) - 3
                print(f"     ... +{remaining} more items")
            print()

    def create_new_project(self):
        """Create a new project in pending-updates"""
        print(f"{Colors.HEADER}🆕 CREATE NEW PROJECT{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        
        project_name = input(f"{Colors.OKCYAN}Enter project name: {Colors.ENDC}").strip()
        if not project_name:
            print(f"{Colors.FAIL}❌ Project name cannot be empty.{Colors.ENDC}")
            return
        
        # Sanitize project name
        safe_name = "".join(c for c in project_name if c.isalnum() or c in "-_").lower()
        if safe_name != project_name:
            print(f"{Colors.WARNING}⚠️  Project name sanitized to: {safe_name}{Colors.ENDC}")
        
        project_dir = self.pending_dir / safe_name
        
        if project_dir.exists():
            print(f"{Colors.FAIL}❌ Project '{safe_name}' already exists.{Colors.ENDC}")
            return
        
        # Create project directory
        project_dir.mkdir()
        
        # Choose project type
        print(f"\n{Colors.OKGREEN}📋 SELECT PROJECT TYPE:{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}1.{Colors.ENDC} React Component (TSX)")
        print(f"  {Colors.OKCYAN}2.{Colors.ENDC} Single HTML Page (Dan's Pattern)")
        print(f"  {Colors.OKCYAN}3.{Colors.ENDC} Node.js Express App")
        print(f"  {Colors.OKCYAN}4.{Colors.ENDC} Empty project")
        
        choice = input(f"\n{Colors.OKCYAN}Choose project type (1-4): {Colors.ENDC}").strip()
        
        if choice == "1":
            self._create_react_component(project_dir, safe_name)
        elif choice == "2":
            self._create_html_page(project_dir, safe_name)
        elif choice == "3":
            self._create_express_app(project_dir, safe_name)
        elif choice == "4":
            self._create_empty_project(project_dir, safe_name)
        else:
            print(f"{Colors.WARNING}⚠️  Invalid choice. Creating empty project.{Colors.ENDC}")
            self._create_empty_project(project_dir, safe_name)
        
        print(f"\n{Colors.OKGREEN}✅ Project '{safe_name}' created successfully!{Colors.ENDC}")
        print(f"{Colors.OKBLUE}📁 Location: {project_dir}{Colors.ENDC}")

    def _create_react_component(self, project_dir, name):
        """Create a React component project"""
        # Create main component file
        component_content = f'''import React, {{ useState }} from 'react';

const {name.replace('-', '').title()}Component = () => {{
  const [count, setCount] = useState(0);

  return (
    <div className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">{name.replace('-', ' ').title()}</h1>
      <div className="space-y-4">
        <p className="text-gray-600">Count: {{count}}</p>
        <div className="space-x-2">
          <button 
            onClick={{() => setCount(count + 1)}}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Increment
          </button>
          <button 
            onClick={{() => setCount(count - 1)}}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Decrement
          </button>
        </div>
      </div>
    </div>
  );
}};

export default {name.replace('-', '').title()}Component;
'''
        
        (project_dir / f"{name}.tsx").write_text(component_content)
        
        # Create package.json
        package_json = {
            "name": name,
            "version": "1.0.0",
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "devDependencies": {
                "typescript": "^5.0.0",
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0"
            }
        }
        
        (project_dir / "package.json").write_text(json.dumps(package_json, indent=2))
        
        # Create README
        readme_content = f'''# {name.replace('-', ' ').title()}

A React component created with G.A.R.D.E.N. Deploy Manager.

## Usage

```tsx
import {name.replace('-', '').title()}Component from './{name}';

function App() {{
  return <{name.replace('-', '').title()}Component />;
}}
```

## Development

This component was generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} using the G.A.R.D.E.N. project management system.
'''
        
        (project_dir / "README.md").write_text(readme_content)

    def _create_html_page(self, project_dir, name):
        """Create a single HTML page following Dan's pattern"""
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name.replace('-', ' ').title()}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2563eb;
            margin-bottom: 1rem;
        }}
        
        .button {{
            background: #2563eb;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        
        .button:hover {{
            background: #1d4ed8;
        }}
        
        .status {{
            margin-top: 1rem;
            padding: 1rem;
            background: #f0f9ff;
            border-left: 4px solid #2563eb;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{name.replace('-', ' ').title()}</h1>
        <p>This is a single-file application created with G.A.R.D.E.N. Deploy Manager following Dan's NodePad pattern.</p>
        
        <div style="margin: 2rem 0;">
            <button class="button" onclick="handleAction()">Click Me!</button>
        </div>
        
        <div id="status" class="status" style="display: none;">
            <strong>Action performed!</strong> Time: <span id="timestamp"></span>
        </div>
    </div>

    <script>
        function handleAction() {{
            const status = document.getElementById('status');
            const timestamp = document.getElementById('timestamp');
            
            timestamp.textContent = new Date().toLocaleString();
            status.style.display = 'block';
            
            console.log('{name.replace('-', ' ').title()} action performed at', new Date());
        }}
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('{name.replace('-', ' ').title()} initialized');
        }});
    </script>
</body>
</html>'''
        
        (project_dir / f"{name}.html").write_text(html_content)

    def _create_express_app(self, project_dir, name):
        """Create a Node.js Express application"""
        # Create main app file
        app_content = f'''const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Routes
app.get('/', (req, res) => {{
    res.json({{
        message: 'Welcome to {name.replace('-', ' ').title()}',
        timestamp: new Date().toISOString(),
        endpoints: [
            'GET / - This message',
            'GET /health - Health check',
            'POST /api/data - Submit data'
        ]
    }});
}});

app.get('/health', (req, res) => {{
    res.json({{ status: 'healthy', timestamp: new Date().toISOString() }});
}});

app.post('/api/data', (req, res) => {{
    const {{ data }} = req.body;
    console.log('Received data:', data);
    res.json({{ success: true, received: data, timestamp: new Date().toISOString() }});
}});

app.listen(PORT, () => {{
    console.log(`{name.replace('-', ' ').title()} running on port ${{PORT}}`);
}});
'''
        
        (project_dir / "app.js").write_text(app_content)
        
        # Create package.json
        package_json = {
            "name": name,
            "version": "1.0.0",
            "description": f"{name.replace('-', ' ').title()} - Express API",
            "main": "app.js",
            "scripts": {
                "start": "node app.js",
                "dev": "nodemon app.js"
            },
            "dependencies": {
                "express": "^4.18.0"
            },
            "devDependencies": {
                "nodemon": "^3.0.0"
            }
        }
        
        (project_dir / "package.json").write_text(json.dumps(package_json, indent=2))

    def _create_empty_project(self, project_dir, name):
        """Create an empty project with basic structure"""
        readme_content = f'''# {name.replace('-', ' ').title()}

Empty project created with G.A.R.D.E.N. Deploy Manager.

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Next Steps

Add your project files to this directory:
- Source code files
- Configuration files  
- Documentation
- Assets

## Deployment

Use the G.A.R.D.E.N. Deploy Manager to deploy this project when ready.
'''
        
        (project_dir / "README.md").write_text(readme_content)
        (project_dir / ".gitkeep").write_text("")

    def view_project_details(self):
        """View detailed information about a specific project"""
        print(f"{Colors.HEADER}📋 PROJECT DETAILS{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        
        projects = [d for d in self.pending_dir.iterdir() if d.is_dir()]
        
        if not projects:
            print(f"{Colors.WARNING}No projects found.{Colors.ENDC}")
            return
        
        print(f"{Colors.OKGREEN}Available projects:{Colors.ENDC}")
        for i, project in enumerate(projects, 1):
            print(f"  {Colors.OKCYAN}{i}.{Colors.ENDC} {project.name}")
        
        try:
            choice = int(input(f"\n{Colors.OKCYAN}Select project number: {Colors.ENDC}")) - 1
            if 0 <= choice < len(projects):
                project = projects[choice]
                self._show_project_details(project)
            else:
                print(f"{Colors.FAIL}❌ Invalid project number.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}❌ Please enter a valid number.{Colors.ENDC}")

    def _show_project_details(self, project_path):
        """Show detailed information about a project"""
        print(f"\n{Colors.BOLD}📁 PROJECT: {project_path.name}{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Location: {project_path}{Colors.ENDC}")
        
        # Show file tree
        print(f"\n{Colors.OKGREEN}📂 Files and directories:{Colors.ENDC}")
        self._show_tree(project_path, prefix="")
        
        # Show git status if it's a git repo
        if (project_path / ".git").exists():
            print(f"\n{Colors.OKGREEN}📊 Git Status:{Colors.ENDC}")
            try:
                result = subprocess.run(
                    ["git", "status", "--short"], 
                    cwd=project_path, 
                    capture_output=True, 
                    text=True
                )
                if result.stdout:
                    print(result.stdout)
                else:
                    print("Working directory clean")
            except subprocess.SubprocessError:
                print("Could not get git status")

    def _show_tree(self, path, prefix="", max_depth=3, current_depth=0):
        """Recursively show directory tree"""
        if current_depth >= max_depth:
            return
        
        items = sorted(path.iterdir())
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            
            if item.is_dir():
                print(f"{prefix}{'└── ' if is_last else '├── '}📁 {item.name}/")
                if current_depth < max_depth - 1:
                    extension = "    " if is_last else "│   "
                    self._show_tree(item, prefix + extension, max_depth, current_depth + 1)
            else:
                print(f"{prefix}{'└── ' if is_last else '├── '}📄 {item.name}")

    def deploy_to_vercel(self):
        """Deploy a project to Vercel"""
        print(f"{Colors.HEADER}🚀 DEPLOY TO VERCEL{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        print(f"{Colors.WARNING}⚠️  This feature will be implemented in Phase 2{Colors.ENDC}")
        print(f"{Colors.OKBLUE}For now, manually deploy using:{Colors.ENDC}")
        print(f"  1. Copy project to separate directory")
        print(f"  2. Run: vercel --prod")
        print(f"  3. Follow Vercel prompts")

    def initialize_git(self):
        """Initialize or check Git repository"""
        print(f"{Colors.HEADER}📊 GIT REPOSITORY STATUS{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        
        if (self.root_dir / ".git").exists():
            print(f"{Colors.OKGREEN}✅ Git repository already initialized{Colors.ENDC}")
            
            try:
                # Show git status
                result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
                if result.stdout:
                    print(f"\n{Colors.OKBLUE}📋 Current status:{Colors.ENDC}")
                    print(result.stdout)
                else:
                    print(f"{Colors.OKGREEN}Working directory clean{Colors.ENDC}")
                
                # Show recent commits
                result = subprocess.run(
                    ["git", "log", "--oneline", "-5"], 
                    capture_output=True, 
                    text=True
                )
                if result.stdout:
                    print(f"\n{Colors.OKBLUE}📜 Recent commits:{Colors.ENDC}")
                    print(result.stdout)
                    
            except subprocess.SubprocessError:
                print(f"{Colors.WARNING}⚠️  Could not get git status{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}⚠️  No git repository found{Colors.ENDC}")
            
            if input(f"{Colors.OKCYAN}Initialize git repository? (y/N): {Colors.ENDC}").lower() == 'y':
                try:
                    subprocess.run(["git", "init"], check=True)
                    print(f"{Colors.OKGREEN}✅ Git repository initialized{Colors.ENDC}")
                    
                    # Create initial .gitignore
                    gitignore_content = """# Dependencies
node_modules/
*.log

# Build outputs
dist/
build/
out/

# Environment files
.env
.env.local

# OS files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Deployment
.vercel/
.netlify/
"""
                    (self.root_dir / ".gitignore").write_text(gitignore_content)
                    print(f"{Colors.OKGREEN}✅ .gitignore created{Colors.ENDC}")
                    
                except subprocess.SubprocessError as e:
                    print(f"{Colors.FAIL}❌ Failed to initialize git: {e}{Colors.ENDC}")

    def create_web_uploader(self):
        """Create the web uploader interface"""
        print(f"{Colors.HEADER}🌐 CREATE WEB UPLOADER INTERFACE{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        print(f"{Colors.WARNING}⚠️  Web uploader will be created next...{Colors.ENDC}")
        print(f"{Colors.OKBLUE}This will create a drag & drop interface for project uploads{Colors.ENDC}")

    def system_status(self):
        """Show system status and configuration"""
        print(f"{Colors.HEADER}📊 SYSTEM STATUS{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        
        print(f"{Colors.OKGREEN}📁 Directory Structure:{Colors.ENDC}")
        print(f"  Root: {self.root_dir}")
        print(f"  Pending: {self.pending_dir} ({'✅' if self.pending_dir.exists() else '❌'})")
        print(f"  Deployed: {self.deployed_dir} ({'✅' if self.deployed_dir.exists() else '❌'})")
        print(f"  Templates: {self.templates_dir} ({'✅' if self.templates_dir.exists() else '❌'})")
        
        # Count projects
        pending_count = len([d for d in self.pending_dir.iterdir() if d.is_dir()]) if self.pending_dir.exists() else 0
        deployed_count = len([d for d in self.deployed_dir.iterdir() if d.is_dir()]) if self.deployed_dir.exists() else 0
        
        print(f"\n{Colors.OKGREEN}📊 Project Counts:{Colors.ENDC}")
        print(f"  Pending projects: {pending_count}")
        print(f"  Deployed projects: {deployed_count}")
        
        print(f"\n{Colors.OKGREEN}🐍 Python Environment:{Colors.ENDC}")
        print(f"  Python version: {sys.version}")
        print(f"  Python executable: {sys.executable}")
        
        print(f"\n{Colors.OKGREEN}📋 Available Commands:{Colors.ENDC}")
        print(f"  Git: {'✅' if shutil.which('git') else '❌'}")
        print(f"  Node: {'✅' if shutil.which('node') else '❌'}")
        print(f"  NPM: {'✅' if shutil.which('npm') else '❌'}")
        print(f"  Vercel CLI: {'✅' if shutil.which('vercel') else '❌'}")

    def export_project_list(self):
        """Export project list to JSON"""
        print(f"{Colors.HEADER}📤 EXPORT PROJECT LIST{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        
        projects_data = {
            "exported_at": datetime.now().isoformat(),
            "system_info": {
                "root_directory": str(self.root_dir),
                "python_version": sys.version,
                "platform": sys.platform
            },
            "pending_projects": [],
            "deployed_projects": []
        }
        
        # Collect pending projects
        if self.pending_dir.exists():
            for project_dir in self.pending_dir.iterdir():
                if project_dir.is_dir():
                    files = [f.name for f in project_dir.iterdir()]
                    projects_data["pending_projects"].append({
                        "name": project_dir.name,
                        "path": str(project_dir),
                        "files": files,
                        "file_count": len(files)
                    })
        
        # Collect deployed projects
        if self.deployed_dir.exists():
            for project_dir in self.deployed_dir.iterdir():
                if project_dir.is_dir():
                    files = [f.name for f in project_dir.iterdir()]
                    projects_data["deployed_projects"].append({
                        "name": project_dir.name,
                        "path": str(project_dir),
                        "files": files,
                        "file_count": len(files)
                    })
        
        # Save export
        export_file = self.root_dir / f"garden-projects-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        export_file.write_text(json.dumps(projects_data, indent=2))
        
        print(f"{Colors.OKGREEN}✅ Project list exported to: {export_file}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}📊 Summary:{Colors.ENDC}")
        print(f"  Pending projects: {len(projects_data['pending_projects'])}")
        print(f"  Deployed projects: {len(projects_data['deployed_projects'])}")

    def backup_projects(self):
        """Create backup of all projects"""
        print(f"{Colors.HEADER}💾 BACKUP PROJECTS{Colors.ENDC}")
        print(f"{Colors.BOLD}─────────────────────────────────────{Colors.ENDC}")
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_dir = self.root_dir / f"garden-backup-{timestamp}"
        
        try:
            backup_dir.mkdir()
            
            # Copy pending projects
            if self.pending_dir.exists():
                shutil.copytree(self.pending_dir, backup_dir / "pending-updates")
                print(f"{Colors.OKGREEN}✅ Pending projects backed up{Colors.ENDC}")
            
            # Copy deployed projects
            if self.deployed_dir.exists():
                shutil.copytree(self.deployed_dir, backup_dir / "deployed-projects")
                print(f"{Colors.OKGREEN}✅ Deployed projects backed up{Colors.ENDC}")
            
            # Copy templates if they exist
            if self.templates_dir.exists() and any(self.templates_dir.iterdir()):
                shutil.copytree(self.templates_dir, backup_dir / "project-templates")
                print(f"{Colors.OKGREEN}✅ Templates backed up{Colors.ENDC}")
            
            # Create backup manifest
            manifest = {
                "backup_created": datetime.now().isoformat(),
                "source_directory": str(self.root_dir),
                "backup_directory": str(backup_dir),
                "contents": [
                    d.name for d in backup_dir.iterdir()
                ]
            }
            
            (backup_dir / "backup-manifest.json").write_text(json.dumps(manifest, indent=2))
            
            print(f"\n{Colors.OKGREEN}✅ Backup completed successfully!{Colors.ENDC}")
            print(f"{Colors.OKBLUE}📁 Backup location: {backup_dir}{Colors.ENDC}")
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Backup failed: {e}{Colors.ENDC}")

    def run(self):
        """Main menu loop"""
        while True:
            try:
                self.show_menu()
                choice = input(f"{Colors.OKCYAN}Enter your choice (0-9): {Colors.ENDC}").strip()
                
                if choice == "0":
                    print(f"\n{Colors.OKGREEN}👋 Thank you for using G.A.R.D.E.N. Deploy Manager!{Colors.ENDC}")
                    print(f"{Colors.OKBLUE}🌱 Happy coding!{Colors.ENDC}")
                    break
                elif choice == "1":
                    self.list_pending_projects()
                elif choice == "2":
                    self.create_new_project()
                elif choice == "3":
                    self.view_project_details()
                elif choice == "4":
                    self.deploy_to_vercel()
                elif choice == "5":
                    self.initialize_git()
                elif choice == "6":
                    self.create_web_uploader()
                elif choice == "7":
                    self.system_status()
                elif choice == "8":
                    self.export_project_list()
                elif choice == "9":
                    self.backup_projects()
                else:
                    print(f"{Colors.WARNING}⚠️  Invalid choice. Please enter 0-9.{Colors.ENDC}")
                
                # Wait for user to continue (except for exit)
                if choice != "0":
                    input(f"\n{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")
                    print()  # Add spacing between operations
                    
            except KeyboardInterrupt:
                print(f"\n\n{Colors.WARNING}⚠️  Operation cancelled by user.{Colors.ENDC}")
                print(f"{Colors.OKGREEN}👋 Goodbye!{Colors.ENDC}")
                break
            except Exception as e:
                print(f"{Colors.FAIL}❌ An error occurred: {e}{Colors.ENDC}")
                input(f"{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")


def main():
    """Entry point for the application"""
    try:
        # Check if we're in the right directory
        current_dir = Path.cwd()
        if not (current_dir.name == "garden-projects" or 
                any(d.name == "pending-updates" for d in current_dir.iterdir() if d.is_dir())):
            print(f"{Colors.WARNING}⚠️  Warning: You may not be in the garden-projects directory.{Colors.ENDC}")
            print(f"{Colors.OKBLUE}Current directory: {current_dir}{Colors.ENDC}")
            
            response = input(f"{Colors.OKCYAN}Continue anyway? (y/N): {Colors.ENDC}")
            if response.lower() != 'y':
                print(f"{Colors.OKGREEN}👋 Please navigate to your garden-projects directory and try again.{Colors.ENDC}")
                return
        
        # Initialize and run the deploy manager
        manager = GARDENDeployManager()
        manager.run()
        
    except Exception as e:
        print(f"{Colors.FAIL}❌ Fatal error: {e}{Colors.ENDC}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())