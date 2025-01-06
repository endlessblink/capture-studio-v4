# Git Development Guidelines

## Branch Management

### Branch Types
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent production fixes

### Branch Naming
- Use descriptive, hyphen-separated names
- Include ticket/issue number if applicable
- Examples:
  - `feature/close-button`
  - `bugfix/toolbar-icons`
  - `hotfix/crash-fix-123`

## Commit Guidelines

### Commit Structure
1. Keep commits small and focused
2. One logical change per commit
3. Separate refactoring from feature changes

### Commit Messages
- First line: Brief summary (50 chars max)
- Leave one blank line
- Detailed description (if needed)
- Example:
  ```
  Add close button to toolbar

  - Added close icon SVG
  - Implemented click handler
  - Updated toolbar layout
  - Added hover effects
  ```

## Development Workflow

### Starting New Work
1. Update main branch:
   ```bash
   git checkout main
   git pull origin main
   ```

2. Create feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```

### During Development
1. Commit frequently:
   ```bash
   git add <specific-files>
   git commit -m "Descriptive message"
   ```

2. Stay updated with main:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

### Before Pushing
1. Review changes:
   ```bash
   git status
   git diff
   ```

2. Run tests and linting
3. Squash commits if needed:
   ```bash
   git rebase -i HEAD~n
   ```

### Pushing Changes
1. Push to feature branch:
   ```bash
   git push origin feature/new-feature
   ```

2. Create pull request
3. Address review comments
4. Merge only when approved

## Conflict Prevention

### Best Practices
1. Pull frequently from main
2. Keep feature branches short-lived
3. Communicate with team about file changes
4. Use `.gitignore` properly

### .gitignore Management
```
# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project specific
*.backup
resources_rc.py
```

## Code Review Guidelines

### Before Requesting Review
1. Self-review your changes
2. Update documentation if needed
3. Ensure all tests pass
4. Check for style consistency

### During Review
1. Respond to all comments
2. Make requested changes in new commits
3. Push changes to same branch
4. Request re-review when ready

## Emergency Procedures

### If Something Goes Wrong
1. Don't panic
2. Stop making changes
3. Save your work:
   ```bash
   git stash
   ```
4. Get help from team lead

### Recovering from Mistakes
- Undo last commit (keep changes):
  ```bash
  git reset --soft HEAD^
  ```
- Undo last commit (discard changes):
  ```bash
  git reset --hard HEAD^
  ```
- Undo pushed commit:
  ```bash
  git revert <commit-hash>
  ```

## Maintenance

### Regular Tasks
1. Clean up old branches
2. Update .gitignore as needed
3. Review and update documentation
4. Monitor repo size and performance

### Branch Cleanup
```bash
# List merged branches
git branch --merged

# Delete local branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
``` 