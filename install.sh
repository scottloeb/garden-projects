#!/bin/bash

# G.A.R.D.E.N. Project Management System - Complete Installation
# Run this script in your garden-projects directory

echo "🌱 G.A.R.D.E.N. Project Management System - Complete Installation"
echo "=================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [[ ! -d "pending-updates" && ! -f "deploy-manager.py" ]]; then
    echo -e "${YELLOW}⚠️  Warning: You may not be in the garden-projects directory${NC}"
    echo -e "${BLUE}Current directory: $(pwd)${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}👋 Please navigate to your garden-projects directory and try again.${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}📁 Verifying directory structure...${NC}"

# Create directories if they don't exist
mkdir -p pending-updates
mkdir -p deployed-projects
mkdir -p project-templates

echo -e "${GREEN}✅ Directory structure verified${NC}"

# Check Python version
echo -e "${BLUE}🐍 Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python3 not found. Please install Python 3.6 or higher.${NC}"
    exit 1
fi

# Install/upgrade deploy manager if the complete version isn't present
if [[ ! -f "deploy-manager.py" ]] || ! grep -q "def run(self)" deploy-manager.py; then
    echo -e "${BLUE}📦 Installing complete deploy manager...${NC}"
    
    # Create the complete deploy manager (this would be copied from the artifact)
    echo "# Complete deploy manager will be installed here" > deploy-manager-new.py
    echo "# (In a real installation, this would copy the complete version)"
    
    # For now, just ensure the basic version exists
    if [[ ! -f "deploy-manager.py" ]]; then
        cat > deploy-manager.py << 'EOF'
#!/usr/bin/env python3
"""
G.A.R.D.E.N. Deploy Manager - Basic Version
"""

print("🌱 G.A.R.D.E.N. Deploy Manager v1.1")
print("This is the basic version. Please replace with the complete version from Claude.")
print("Run: python3 deploy-manager.py")
EOF
    fi
    
    chmod +x deploy-manager.py
    echo -e "${GREEN}✅ Deploy manager installed${NC}"
else
    echo -e "${GREEN}✅ Deploy manager already installed${NC}"
fi

# Install web uploader if it doesn't exist
if [[ ! -f "garden-uploader.html" ]]; then
    echo -e "${BLUE}🌐 Installing web uploader interface...${NC}"
    
    # Create placeholder (in real installation, this would copy the complete HTML)
    cat > garden-uploader.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>G.A.R.D.E.N. Web Uploader</title>
</head>
<body>
    <h1>🌱 G.A.R.D.E.N. Web Uploader</h1>
    <p>Please replace this with the complete web uploader from Claude.</p>
</body>
</html>
EOF
    
    echo -e "${GREEN}✅ Web uploader installed${NC}"
else
    echo -e "${GREEN}✅ Web uploader already exists${NC}"
fi

# Initialize Git if not already done
if [[ ! -d ".git" ]]; then
    echo -e "${BLUE}📊 Initializing Git repository...${NC}"
    git init
    
    # Create .gitignore
    cat > .gitignore << 'EOF'
# Dependencies
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

# Python
__pycache__/
*.pyc
*.pyo

# Deployment
.vercel/
.netlify/

# Backups
*-backup-*/
EOF
    
    echo -e "${GREEN}✅ Git repository initialized${NC}"
else
    echo -e "${GREEN}✅ Git repository already exists${NC}"
fi

# Check for required tools
echo -e "${BLUE}🔧 Checking for optional tools...${NC}"

if command -v git &> /dev/null; then
    echo -e "${GREEN}✅ Git: $(git --version)${NC}"
else
    echo -e "${YELLOW}⚠️  Git not found (recommended for version control)${NC}"
fi

if command -v node &> /dev/null; then
    echo -e "${GREEN}✅ Node.js: $(node --version)${NC}"
else
    echo -e "${YELLOW}⚠️  Node.js not found (needed for React/Express projects)${NC}"
fi

if command -v npm &> /dev/null; then
    echo -e "${GREEN}✅ NPM: $(npm --version)${NC}"
else
    echo -e "${YELLOW}⚠️  NPM not found (needed for Node.js projects)${NC}"
fi

if command -v vercel &> /dev/null; then
    echo -e "${GREEN}✅ Vercel CLI: $(vercel --version)${NC}"
else
    echo -e "${YELLOW}⚠️  Vercel CLI not found (install with: npm i -g vercel)${NC}"
fi

# Create a test project if none exist
if [[ ! -d "pending-updates/test-project" ]]; then
    echo -e "${BLUE}🧪 Creating test project...${NC}"
    
    mkdir -p pending-updates/test-project
    
    cat > pending-updates/test-project/README.md << 'EOF'
# Test Project

This is a test project created during G.A.R.D.E.N. installation.

## Created
EOF
    echo "$(date)" >> pending-updates/test-project/README.md
    
    cat > pending-updates/test-project/test.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>G.A.R.D.E.N. Test Project</title>
    <style>
        body { font-family: system-ui; text-align: center; padding: 2rem; }
        h1 { color: #4a6fa5; }
    </style>
</head>
<body>
    <h1>🌱 G.A.R.D.E.N. Test Project</h1>
    <p>This test project was created during installation.</p>
    <p>You can deploy this to test your setup!</p>
</body>
</html>
EOF
    
    echo -e "${GREEN}✅ Test project created${NC}"
fi

# Show status summary
echo
echo -e "${GREEN}🎉 G.A.R.D.E.N. Installation Complete!${NC}"
echo "======================================="
echo
echo -e "${BLUE}📁 Directory Structure:${NC}"
echo "  $(pwd)/"
echo "  ├── deploy-manager.py        (CLI management tool)"
echo "  ├── garden-uploader.html     (Web interface)"
echo "  ├── pending-updates/         (Source projects)"
echo "  ├── deployed-projects/       (Deployed projects)"
echo "  └── project-templates/       (Project templates)"
echo
echo -e "${BLUE}🚀 Quick Start:${NC}"
echo "  1. Run CLI manager:    python3 deploy-manager.py"
echo "  2. Open web interface: open garden-uploader.html"
echo "  3. Create new project: Choose option 2 in CLI"
echo "  4. Upload files:       Use web interface drag & drop"
echo
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "  • Replace deploy-manager.py with complete version from Claude"
echo "  • Replace garden-uploader.html with complete version from Claude"
echo "  • Install Vercel CLI: npm install -g vercel"
echo "  • Test deployment with the test project"
echo
echo -e "${BLUE}🆘 Need Help?${NC}"
echo "  • Run: python3 deploy-manager.py (option 7 for system status)"
echo "  • Open: garden-uploader.html (click ? button for help)"
echo "  • Check: README.md files in each project"
echo
echo -e "${GREEN}✨ Happy coding with G.A.R.D.E.N.! 🌱${NC}"