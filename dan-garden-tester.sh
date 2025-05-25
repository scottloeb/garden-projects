#!/bin/bash

# G.A.R.D.E.N. Testing Setup for Dan
# Single-file deployment for comprehensive testing
# Version 1.5 - Post-Vercel Deployment

set -e  # Exit on any error

echo "🌱 G.A.R.D.E.N. Testing Environment Setup for Dan"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check system requirements
echo "🔧 Checking System Requirements..."
echo "=================================="

# Check for Python 3
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_status "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.6+ before continuing."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check for Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version 2>&1)
    print_status "Git found: $GIT_VERSION"
else
    print_error "Git not found. Please install Git before continuing."
    echo "Visit: https://git-scm.com/downloads"
    exit 1
fi

# Check for web browser
if command -v open &> /dev/null; then
    print_status "macOS detected - 'open' command available"
elif command -v xdg-open &> /dev/null; then
    print_status "Linux detected - 'xdg-open' command available"
elif command -v start &> /dev/null; then
    print_status "Windows detected - 'start' command available"
else
    print_warning "Browser opening commands not detected - you'll need to open URLs manually"
fi

echo ""

# Create directory structure
echo "📁 Creating G.A.R.D.E.N. Testing Environment..."
echo "=============================================="

# Create main directory
TEST_DIR="garden-testing-dan"
if [ -d "$TEST_DIR" ]; then
    print_warning "Directory $TEST_DIR already exists. Creating backup..."
    mv "$TEST_DIR" "${TEST_DIR}-backup-$(date +%Y%m%d-%H%M%S)"
fi

mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

print_status "Created testing directory: $TEST_DIR"

# Create subdirectories
mkdir -p {test-projects,test-results,documentation,scripts}
print_status "Created subdirectories"

echo ""

# Create comprehensive testing plan
echo "📋 Creating Testing Plan..."
echo "=========================="

cat > "DAN-TESTING-PLAN.md" << 'EOF'
# G.A.R.D.E.N. Testing Plan for Dan
## Version 1.5 - Post-Vercel Deployment

### 🎯 OVERVIEW
You're testing the G.A.R.D.E.N. Project Management System which has two main components:
- **CLI Interface** (fully functional - creates real projects)
- **Web Interface** (visual simulation - planning and demonstration)

### 🚀 QUICK START (5 minutes)
1. **Test Web Interface**: Open the Vercel deployment link provided
2. **Test CLI Interface**: Run `python3 deploy-manager.py` in this directory
3. **Create a Test Project**: Use CLI option 1 to create a real project
4. **Submit Feedback**: Use the feedback forms when ready

---

## 📋 DETAILED TESTING WORKFLOWS

### 🌐 WEB INTERFACE TESTING (Vercel Deployment)

**URL**: [Will be provided by Scott]

#### Test Case 1: First Impression & Navigation (5 minutes)
```
□ Open the Vercel link in your browser
□ Check mobile view (resize browser or use phone)
□ Navigate through all 5 tabs: Overview, Create Project, Projects, Upload, Deploy
□ Try keyboard shortcuts: Alt+O, Alt+C, Alt+P, Alt+U, Alt+D, F1
□ Click the floating help button (?)
```
**What to Look For:**
- Does the interface feel professional and polished?
- Is the messaging about CLI vs. web functionality clear?
- Are the keyboard shortcuts working? (Known issue - please test anyway)
- Is navigation intuitive on both desktop and mobile?

#### Test Case 2: Project Creation Simulation (10 minutes)
```
□ Go to "Create Project" tab
□ Enter project name: "dan-test-app"
□ Add description: "Testing the project creation workflow"
□ Select different templates (React, HTML, Express, Empty)
□ Click "Create Project (Simulation)"
□ Try creating project without name (should show error)
```
**What to Look For:**
- Are the templates clearly differentiated?
- Is the "simulation" messaging clear and not misleading?
- Do error messages make sense?
- Would you understand what to do next?

#### Test Case 3: File Upload Simulation (10 minutes)
```
□ Go to "Upload Files" tab
□ Try drag & drop with various file types (.html, .js, .txt, .exe)
□ Try clicking "select files" and choosing multiple files
□ Watch progress bars during simulation
□ Try uploading without selecting files (should show error)
□ Clear the file list
```
**What to Look For:**
- Does drag & drop feel natural?
- Are file validations working (rejecting .exe files, etc.)?
- Are progress bars smooth and realistic?
- Is the "simulation only" messaging clear?

#### Test Case 4: Overall User Experience (10 minutes)
```
□ Spend time exploring without specific tasks
□ Look for anything confusing or unclear
□ Test on different browsers if possible (Chrome, Safari, Firefox)
□ Check if you can understand the G.A.R.D.E.N. philosophy from the interface
```

### 🖥️ CLI INTERFACE TESTING (Real Functionality)

#### Test Case 5: CLI Setup & First Run (5 minutes)
```
□ Open terminal/command prompt in this directory
□ Run: python3 deploy-manager.py
□ Navigate through the menu (try options 2, 8 for safe exploration)
□ Exit with option 0
```
**What to Look For:**
- Does the CLI interface feel intuitive?
- Are menu options clearly explained?
- Is the color coding helpful?
- Any error messages or unexpected behavior?

#### Test Case 6: Real Project Creation (15 minutes)
```
□ Run: python3 deploy-manager.py
□ Choose option 1: "Create new project"
□ Project name: "dan-real-test"
□ Description: "Testing real project creation"
□ Choose template: HTML (Dan's Pattern) - recommended
□ Let it create the project
□ Option 2: "List existing projects" to see your new project
□ Navigate to test-projects/ folder to see the actual files
```
**What to Look For:**
- Does project creation feel smooth and professional?
- Are the generated files what you'd expect?
- Is the HTML file (if chosen) a complete, working application?
- Can you open the HTML file directly in a browser?

#### Test Case 7: Advanced CLI Features (10 minutes)
```
□ Try option 8: "System status" to see tool verification
□ Try option 4: "Backup projects" to create a backup
□ Try option 5: "Export project" with your test project
□ Explore any other options that seem interesting
```
**What to Look For:**
- Do advanced features work as expected?
- Are error messages helpful if something goes wrong?
- Is the system status information useful?

---

## 🐛 BUG REPORTING & FEATURE REQUESTS

### 🚨 Known Issues (Please Test Anyway)
- **Keyboard shortcuts** may not work in web interface on some browsers
- **File upload** simulation may have browser compatibility issues
- **Permission errors** in browser console are expected (security restrictions)

### 📝 How to Submit Feedback

**For Bugs:**
1. Note what you were trying to do
2. What happened vs. what you expected
3. Browser/system info if relevant
4. Screenshots if helpful

**For Feature Requests:**
1. Describe the feature you'd like
2. Explain the use case (why it would be helpful)
3. Any implementation ideas

**Where to Submit:**
- Use the GitHub repository: [Scott will provide link]
- Create new issues with "Bug" or "Enhancement" labels
- OR email Scott directly with feedback

---

## 🎯 WHAT I'M MOST INTERESTED IN

### Critical Questions:
1. **Is the CLI vs. Web distinction clear?** Do you understand what's real vs. simulation?
2. **Does the CLI feel production-ready?** Would you use it for real projects?
3. **Is the web interface helpful for planning?** Even without real file creation?
4. **What's confusing or unclear?** Where did you get stuck or have questions?
5. **What's missing?** What features would make this significantly more useful?

### G.A.R.D.E.N. Philosophy Questions:
1. **Cognitive Alignment**: Do the interfaces match how you think about project management?
2. **Technical Abstraction**: Is complexity appropriately hidden while maintaining power?
3. **Progressive Discovery**: Can you start simple and discover advanced features naturally?
4. **Multiple Perspectives**: Do CLI and web interfaces complement each other well?

---

## 🚀 NEXT STEPS AFTER TESTING

### If You Want to Build On This:
1. **Fork the repository** (link provided by Scott)
2. **Create your own projects** using the CLI
3. **Modify templates** to fit your needs
4. **Deploy to your own Vercel** account

### If You Want to Contribute:
1. **Submit detailed feedback** via GitHub issues
2. **Suggest improvements** for Phase 2 development
3. **Share use cases** we haven't considered
4. **Test with your actual projects** and report results

---

## ⏱️ TIME ESTIMATES

**Minimum Useful Test**: 30 minutes (Quick Start + one detailed workflow)
**Comprehensive Test**: 90 minutes (all test cases)
**Deep Exploration**: 2-3 hours (including building real projects)

Start with whatever time you have - even 15 minutes of feedback is valuable!

---

## 🆘 GETTING HELP

**If Something Doesn't Work:**
1. Check system requirements above
2. Try restarting terminal/browser
3. Look for error messages and include them in feedback
4. Contact Scott with specific details

**If You're Not Sure What to Test:**
1. Start with the Quick Start section
2. Focus on Test Cases 1, 2, and 5
3. Ask questions - that's valuable feedback too!

**If You Want to Go Deeper:**
1. Try creating multiple projects with different templates
2. Explore the generated files and modify them
3. Think about how this could fit into your workflow
4. Imagine what features would make it irresistible

---

Thank you for testing G.A.R.D.E.N.! Your feedback will directly shape Phase 2 development.
EOF

print_status "Created comprehensive testing plan: DAN-TESTING-PLAN.md"

# Create system requirements documentation
cat > "SYSTEM-REQUIREMENTS.md" << 'EOF'
# System Requirements for G.A.R.D.E.N. Testing

## ✅ Required Software
- **Python 3.6+** (for CLI interface)
- **Git** (for repository management)
- **Modern Web Browser** (Chrome, Safari, Firefox, Edge)

## 🖥️ Supported Operating Systems
- **macOS** 10.12+ (fully tested)
- **Linux** Ubuntu 18.04+ (compatible)
- **Windows** 10+ (compatible, use `python` instead of `python3`)

## 🌐 Web Interface Requirements
- **Internet Connection** (for Vercel deployment access)
- **JavaScript Enabled** (for interactive features)
- **Local Storage** (for preferences, automatically available)

## 📱 Mobile Testing
- **iOS Safari** 12+ (responsive design tested)
- **Android Chrome** 80+ (responsive design tested)
- **Touch Interactions** supported for all major features

## 🚫 Not Required
- **Node.js** (CLI uses pure Python)
- **Package Managers** (npm, yarn, etc.)
- **Build Tools** (webpack, vite, etc.)
- **Database** (uses file system and localStorage)

## ⚠️ Known Compatibility Issues
- **Older Internet Explorer** (not supported)
- **Very Old Mobile Browsers** (may have limited functionality)
- **Corporate Firewalls** (may block Vercel deployment access)

The system is designed to work with minimal dependencies and maximum compatibility.
EOF

print_status "Created system requirements: SYSTEM-REQUIREMENTS.md"

# Create development roadmap
cat > "DEVELOPMENT-ROADMAP.md" << 'EOF'
# G.A.R.D.E.N. Development Roadmap
## Post-Phase 1.5 Planning

### ✅ COMPLETED (Phase 1.5)
- **CLI Interface**: Complete menu system with real project creation
- **Web Interface**: Professional UI with simulation and clear guidance
- **Project Templates**: React, HTML (Dan's Pattern), Express, Empty
- **File Management**: Upload, organize, backup systems
- **Documentation**: Comprehensive guides and testing plans
- **Deployment**: Vercel-ready single-file architecture

---

## 🚀 PHASE 2: Enhanced Feedback & Validation (Next 2-3 weeks)

### 🔥 HIGH PRIORITY
1. **Feedback System Integration**
   - Bug report forms → GitHub Issues
   - Feature request workflow
   - Auto-routing and labeling
   - Response tracking

2. **File Upload Bulletproofing**
   - Comprehensive validation testing
   - Error handling and recovery
   - Security validation
   - Cross-browser compatibility

3. **Keyboard Shortcuts Debug**
   - Event listener investigation
   - Browser compatibility fixes
   - Alternative implementation approaches

### 📊 Success Metrics for Phase 2
- Seamless bug reporting workflow
- Zero false positives in file validation
- 90%+ cross-browser compatibility
- Clear user feedback collection

---

## 🔄 PHASE 3: Backend Integration (4-6 weeks)

### 🎯 MAJOR FEATURES
1. **Real Web Interface File Operations**
   - WebSocket connection to CLI backend
   - Real-time project creation from web
   - Actual file uploads to project directories
   - Status synchronization between interfaces

2. **Advanced Project Management**
   - Project templates with customization
   - Dependency management
   - Build process integration
   - Version control automation

3. **Automated Deployment Pipeline**
   - One-click Vercel deployment
   - Environment variable management
   - Domain configuration
   - SSL certificate handling

---

## 🌟 PHASE 4: Advanced Features (Future)

### 🧠 AI-Powered Enhancements
- Project template generation from descriptions
- Code review and optimization suggestions
- Automated documentation generation
- Smart dependency management

### 🌐 Collaboration Features
- Multi-user project management
- Real-time collaborative editing
- Project sharing and permissions
- Team dashboard and analytics

### 🔌 Integration Ecosystem
- GitHub Actions workflow generation
- Docker containerization support
- CI/CD pipeline automation
- Third-party service integrations

---

## 💡 RESEARCH & EXPLORATION

### 🧪 Experimental Features (Dan's Input Welcome)
- Voice-controlled project creation
- Visual programming interface
- Mobile app development
- Desktop application (Electron)

### 🎨 Design Evolution
- Advanced theming system
- Accessibility improvements
- Performance optimization
- User experience refinements

---

## 🤝 CONTRIBUTION OPPORTUNITIES

### 🐛 Testing & Feedback (Current)
- Comprehensive workflow testing
- Bug identification and reporting
- Feature request prioritization
- User experience evaluation

### 💻 Development (Future)
- Template creation and sharing
- Plugin development system
- Custom workflow automation
- Documentation improvements

### 🌱 Community Building
- Example project galleries
- Tutorial and guide creation
- Best practices documentation
- User support systems

---

## 📈 LONG-TERM VISION

### 🎯 Year 1 Goals
- **1000+ active users** across CLI and web interfaces
- **50+ project templates** covering major frameworks
- **10+ integrations** with popular development tools
- **99.9% uptime** for web services

### 🌍 Year 2+ Vision
- Industry-standard tool for rapid prototyping
- Educational platform for learning development workflows
- Open-source ecosystem with community contributions
- Enterprise features for team collaboration

---

This roadmap is living documentation - your testing feedback will directly influence priorities and timelines.
EOF

print_status "Created development roadmap: DEVELOPMENT-ROADMAP.md"

# Create the CLI deploy manager
cat > "deploy-manager.py" << 'EOF'
#!/usr/bin/env python3
"""
G.A.R.D.E.N. Deploy Manager - Testing Version for Dan
Simplified version with core functionality for testing
"""

import os
import sys
import json
import datetime
import subprocess
import shutil
from pathlib import Path

# Colors for terminal output
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

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}🌱 {text}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")

# Project templates
TEMPLATES = {
    "html": {
        "name": "HTML (Dan's Pattern)",
        "description": "Single-file architecture, zero dependencies",
        "files": {
            "index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{PROJECT_NAME}}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: system-ui, -apple-system, sans-serif; 
            line-height: 1.6; 
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            max-width: 600px;
            text-align: center;
        }
        h1 { color: #667eea; margin-bottom: 1rem; }
        p { margin-bottom: 1rem; color: #666; }
        .btn {
            background: #667eea;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        .btn:hover { background: #5a6fd8; }
        .feature-list {
            text-align: left;
            margin: 1.5rem 0;
        }
        .feature-list li {
            margin: 0.5rem 0;
            padding-left: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌱 {{PROJECT_NAME}}</h1>
        <p>{{PROJECT_DESCRIPTION}}</p>
        
        <div class="feature-list">
            <h3>Features Ready to Build:</h3>
            <ul>
                <li>✅ Single-file architecture (Dan's Pattern)</li>
                <li>✅ Zero external dependencies</li>
                <li>✅ Responsive design</li>
                <li>✅ Modern CSS with gradients and shadows</li>
                <li>✅ Interactive JavaScript ready</li>
                <li>✅ Instant deployment to any static host</li>
            </ul>
        </div>
        
        <button class="btn" onclick="startBuilding()">🚀 Start Building</button>
        
        <p style="margin-top: 2rem; font-size: 0.9rem; color: #888;">
            Created with G.A.R.D.E.N. Project Manager<br>
            Generated: {{TIMESTAMP}}
        </p>
    </div>

    <script>
        function startBuilding() {
            alert('🎯 Ready to build! Edit this HTML file to create your application.');
            console.log('🌱 G.A.R.D.E.N. Project: {{PROJECT_NAME}}');
            console.log('📝 Edit this file to start building your application');
            console.log('🚀 Deploy by uploading to Vercel, Netlify, or any static host');
        }
        
        // Log project info for development
        console.log('%c🌱 G.A.R.D.E.N. Project Template', 'color: #667eea; font-size: 16px; font-weight: bold;');
        console.log('Project: {{PROJECT_NAME}}');
        console.log('Description: {{PROJECT_DESCRIPTION}}');
        console.log('Template: HTML (Dan\\'s Pattern)');
        console.log('Generated: {{TIMESTAMP}}');
    </script>
</body>
</html>'''
        }
    },
    "react": {
        "name": "React App",
        "description": "Modern React with hooks and components",
        "files": {
            "package.json": '''{{
  "name": "{{PROJECT_NAME_CLEAN}}",
  "version": "1.0.0",
  "description": "{{PROJECT_DESCRIPTION}}",
  "main": "index.js",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }},
  "devDependencies": {{
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.0.0"
  }}
}}''',
            "index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{PROJECT_NAME}}</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>''',
            "src/main.jsx": '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)''',
            "src/App.jsx": '''import React, { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌱 {{PROJECT_NAME}}</h1>
        <p>{{PROJECT_DESCRIPTION}}</p>
        
        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            Count is {count}
          </button>
          <p>Edit src/App.jsx and save to test HMR</p>
        </div>
        
        <p className="read-the-docs">
          Generated with G.A.R.D.E.N. Project Manager
        </p>
      </header>
    </div>
  )
}

export default App''',
            "src/App.css": '''#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.App {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.App-header {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.card {
  padding: 2em;
}

.read-the-docs {
  color: #888;
  font-size: 0.9rem;
  margin-top: 2rem;
}''',
            "src/index.css": '''body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

button {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
  background-color: #667eea;
  color: white;
  cursor: pointer;
  transition: all 0.25s;
}

button:hover {
  background-color: #5a6fd8;
}'''
        }
    },
    "empty": {
        "name": "Empty Project",
        "description": "Start from scratch",
        "files": {
            "README.md": '''# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

## Getting Started

This is an empty project created with G.A.R.D.E.N. Project Manager.

## Next Steps

1. Add your project files
2. Configure your development environment
3. Start building!

Generated: {{TIMESTAMP}}
'''
        }
    }
}

def create_project():
    """Create a new project with template"""
    print_header("Create New Project")
    
    # Get project details
    project_name = input("Project name (lowercase, hyphens ok): ").strip()
    if not project_name:
        print_error("Project name is required")
        return
    
    # Validate project name
    import re
    if not re.match(r'^[a-z0-9-]+$', project_name):
        print_error("Project name must be lowercase letters, numbers, and hyphens only")
        return
    
    description = input("Project description: ").strip()
    if not description:
        description = f"A new project created with G.A.R.D.E.N."
    
    # Show template options
    print("\nAvailable templates:")
    template_keys = list(TEMPLATES.keys())
    for i, (key, template) in enumerate(TEMPLATES.items()):
        print(f"{i + 1}. {template['name']} - {template['description']}")
    
    # Get template choice
    try:
        choice = int(input(f"\nChoose template (1-{len(template_keys)}): ")) - 1
        if choice < 0 or choice >= len(template_keys):
            raise ValueError()
        template_key = template_keys[choice]
    except (ValueError, IndexError):
        print_error("Invalid template choice")
        return
    
    # Create project directory
    project_dir = Path("test-projects") / project_name
    if project_dir.exists():
        print_error(f"Project {project_name} already exists")
        return
    
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate files from template
    template = TEMPLATES[template_key]
    timestamp = datetime.datetime.now().isoformat()
    
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_NAME_CLEAN}}": project_name.replace("-", ""),
        "{{PROJECT_DESCRIPTION}}": description,
        "{{TIMESTAMP}}": timestamp
    }
    
    for file_path, content in template["files"].items():
        # Apply replacements
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        # Create file
        full_path = project_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
    
    print_success(f"Project '{project_name}' created successfully!")
    print_info(f"Location: {project_dir}")
    print_info(f"Template: {template['name']}")
    
    if template_key == "html":
        print_info(f"You can open {project_dir}/index.html directly in a browser")

def list_projects():
    """List all existing projects"""
    print_header("Existing Projects")
    
    projects_dir = Path("test-projects")
    if not projects_dir.exists():
        print_warning("No projects directory found")
        return
    
    projects = [p for p in projects_dir.iterdir() if p.is_dir()]
    
    if not projects:
        print_warning("No projects found")
        return
    
    for i, project in enumerate(projects):
        print(f"{i + 1}. {project.name}")
        
        # Try to read project info
        readme_path = project / "README.md"
        package_path = project / "package.json"
        index_path = project / "index.html"
        
        if package_path.exists():
            try:
                import json
                with open(package_path) as f:
                    pkg = json.load(f)
                print(f"   Type: {pkg.get('name', 'Unknown')} (React/Node.js)")
                print(f"   Description: {pkg.get('description', 'No description')}")
            except:
                print("   Type: Node.js project")
        elif index_path.exists():
            print("   Type: HTML (Dan's Pattern)")
        elif readme_path.exists():
            print("   Type: Empty/Custom project")
        else:
            print("   Type: Unknown")

def system_status():
    """Check system status and tool availability"""
    print_header("System Status")
    
    # Check Python
    try:
        python_version = sys.version
        print_success(f"Python: {python_version.split()[0]}")
    except:
        print_error("Python version check failed")
    
    # Check Git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"Git: {result.stdout.strip()}")
        else:
            print_error("Git not available")
    except:
        print_error("Git not found")
    
    # Check directory structure
    dirs_to_check = ["test-projects", "test-results", "documentation"]
    for dir_name in dirs_to_check:
        if Path(dir_name).exists():
            print_success(f"Directory {dir_name}: ✓")
        else:
            print_warning(f"Directory {dir_name}: Missing")
    
    # Check for projects
    projects_dir = Path("test-projects")
    if projects_dir.exists():
        project_count = len([p for p in projects_dir.iterdir() if p.is_dir()])
        print_info(f"Projects found: {project_count}")
    else:
        print_info("Projects found: 0")

def main_menu():
    """Display main menu and handle user input"""
    while True:
        print_header("G.A.R.D.E.N. Deploy Manager - Testing Version")
        print("🌱 Graph Algorithms, Research, Development, Enhancement, and Novelties")
        print(f"{Colors.OKCYAN}Testing Environment for Dan{Colors.ENDC}\n")
        
        print("Available options:")
        print("1. 🛠️  Create new project")
        print("2. 📋 List existing projects")
        print("3. 🔍 System status")
        print("4. 📖 Open documentation")
        print("5. 🌐 Open web interface (if available)")
        print("0. 🚪 Exit")
        
        try:
            choice = input(f"\n{Colors.OKBLUE}Choose option (0-5): {Colors.ENDC}").strip()
            
            if choice == "0":
                print_success("Thanks for testing G.A.R.D.E.N.! 🌱")
                break
            elif choice == "1":
                create_project()
            elif choice == "2":
                list_projects()
            elif choice == "3":
                system_status()
            elif choice == "4":
                print_info("Opening documentation files...")
                try:
                    if sys.platform == "darwin":  # macOS
                        subprocess.run(["open", "DAN-TESTING-PLAN.md"])
                    elif sys.platform == "win32":  # Windows
                        subprocess.run(["start", "DAN-TESTING-PLAN.md"], shell=True)
                    else:  # Linux
                        subprocess.run(["xdg-open", "DAN-TESTING-PLAN.md"])
                    print_success("Documentation opened")
                except:
                    print_warning("Could not open documentation automatically")
                    print_info("Please open DAN-TESTING-PLAN.md manually")
            elif choice == "5":
                print_info("Web interface should be accessed via the Vercel deployment")
                print_info("Scott will provide the URL separately")
                vercel_url = input("Enter Vercel URL (or press Enter to skip): ").strip()
                if vercel_url:
                    try:
                        import webbrowser
                        webbrowser.open(vercel_url)
                        print_success("Opening web interface...")
                    except:
                        print_warning("Could not open browser automatically")
                        print_info(f"Please open {vercel_url} manually")
            else:
                print_error("Invalid option. Please choose 0-5.")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Operation cancelled by user{Colors.ENDC}")
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
        
        input(f"\n{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    main_menu()
EOF

print_status "Created CLI deploy manager: deploy-manager.py"

# Create quick start script
cat > "QUICK-START.sh" << 'EOF'
#!/bin/bash

echo "🚀 G.A.R.D.E.N. Quick Start for Dan"
echo "================================="
echo ""
echo "1. 🌐 Test Web Interface:"
echo "   - Open the Vercel URL provided by Scott"
echo "   - Navigate through all tabs"
echo "   - Try creating a project (simulation)"
echo ""
echo "2. 🖥️  Test CLI Interface:"
echo "   python3 deploy-manager.py"
echo ""
echo "3. 📋 Read Testing Plan:"
if command -v open &> /dev/null; then
    echo "   Opening DAN-TESTING-PLAN.md..."
    open DAN-TESTING-PLAN.md
elif command -v xdg-open &> /dev/null; then
    xdg-open DAN-TESTING-PLAN.md
else
    echo "   Please open DAN-TESTING-PLAN.md in your text editor"
fi
echo ""
echo "4. 🐛 Submit Feedback:"
echo "   - Use GitHub issues for bugs/features"
echo "   - Or email Scott directly"
echo ""
echo "Happy testing! 🌱"
EOF

chmod +x QUICK-START.sh
print_status "Created quick start script: QUICK-START.sh"

# Create feedback templates
mkdir -p templates
cat > "templates/bug-report-template.md" << 'EOF'
# Bug Report Template

## 🐛 Bug Description
<!-- Clear description of what's wrong -->

## 🔄 Steps to Reproduce
1. 
2. 
3. 

## ✅ Expected Behavior
<!-- What should have happened -->

## ❌ Actual Behavior
<!-- What actually happened -->

## 🖥️ Environment
- **Browser**: 
- **Operating System**: 
- **Testing Interface**: CLI / Web / Both

## 📸 Screenshots
<!-- If applicable, add screenshots to help explain the problem -->

## 📝 Additional Context
<!-- Any other relevant information -->

---
*Generated by G.A.R.D.E.N. Testing Environment*
EOF

cat > "templates/feature-request-template.md" << 'EOF'
# Feature Request Template

## ✨ Feature Description
<!-- Clear description of the feature you'd like -->

## 🎯 Use Case
<!-- Why would this feature be helpful? What problem does it solve? -->

## 💭 Proposed Implementation
<!-- Any ideas on how this could be implemented -->

## 🚀 Priority Level
- [ ] Nice to have
- [ ] Would be helpful
- [ ] Important for my workflow
- [ ] Critical for adoption

## 📋 Additional Context
<!-- Screenshots, mockups, examples, or other relevant information -->

---
*Generated by G.A.R.D.E.N. Testing Environment*
EOF

print_status "Created feedback templates"

# Create test results directory structure
mkdir -p test-results/{bugs,features,notes}
cat > "test-results/README.md" << 'EOF'
# Test Results Directory

## 📁 Directory Structure
- **bugs/**: Document any bugs found during testing
- **features/**: Note feature requests and ideas
- **notes/**: General testing notes and observations

## 📝 How to Use
1. Create files in appropriate directories
2. Use the templates in ../templates/ as starting points
3. Name files descriptively (e.g., `keyboard-shortcuts-not-working.md`)
4. Submit to GitHub when ready

## 🎯 What We're Looking For
- Usability issues
- Confusing workflows
- Missing features
- Technical problems
- Improvement suggestions

Your feedback directly shapes Phase 2 development!
EOF

print_status "Created test results structure"

# Final status and instructions
echo ""
print_header "Setup Complete! 🎉"
echo ""
print_success "Created testing environment: $TEST_DIR"
print_info "Total files created: $(find . -type f | wc -l)"
echo ""
echo "📋 What Dan should do next:"
echo "1. 📖 Read DAN-TESTING-PLAN.md for detailed instructions"
echo "2. 🚀 Run ./QUICK-START.sh for immediate testing"
echo "3. 🖥️  Test CLI: python3 deploy-manager.py"
echo "4. 🌐 Test Web: Use Vercel URL provided separately"
echo "5. 🐛 Submit feedback via GitHub or email"
echo ""
echo "📞 Contact Scott with questions or when ready to submit feedback"

# Create summary for Scott
cat > "../DAN-SETUP-SUMMARY.txt" << EOF
G.A.R.D.E.N. Testing Setup Complete for Dan
==========================================

Created: $(date)
Location: $(pwd)

📁 Directory Structure:
$(ls -la)

🎯 Key Files for Dan:
- DAN-TESTING-PLAN.md (comprehensive testing guide)
- QUICK-START.sh (immediate start script)
- deploy-manager.py (CLI interface for testing)
- SYSTEM-REQUIREMENTS.md (technical requirements)
- DEVELOPMENT-ROADMAP.md (future planning)

📋 Next Steps for Scott:
1. Send Dan this entire directory
2. Provide Vercel deployment URL
3. Give Dan write access to GitHub repo for feedback
4. Set up GitHub issue templates if not already done

⚠️ GitHub Access Required:
Dan will need write access to the repository to submit GitHub issues.
Alternative: Dan can email feedback directly.

🎉 Status: Ready for Dan's testing!
EOF

print_success "Created summary for Scott: ../DAN-SETUP-SUMMARY.txt"
echo ""
print_info "Dan is ready to test G.A.R.D.E.N.! 🌱"
