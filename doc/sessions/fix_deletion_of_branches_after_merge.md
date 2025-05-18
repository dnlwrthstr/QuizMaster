
# Git Branch Management Solution

To address the issues with branch management, here's a step-by-step solution:

## 1. Check Current Branch Status

First, let's check the current status of branches:

```bash
# List all local branches
git branch

# List all remote branches
git branch -r

# List all branches (both local and remote)
git branch -a
```

## 2. Ensure All Branches Are Merged to Main

```bash
# Switch to main branch
git checkout main

# Make sure main is up to date
git pull origin main

# For each branch that needs to be merged
git checkout <branch-name>
git pull origin <branch-name>
git checkout main
git merge <branch-name>
git push origin main
```

## 3. Delete Branches After Merging

The issue with branch deletion after merging can be fixed by using the correct commands:

### Delete Local Branches

```bash
# Delete a local branch that has been merged
git branch -d <branch-name>

# Force delete a local branch (use with caution)
git branch -D <branch-name>
```

### Delete Remote Branches

```bash
# Delete a remote branch
git push origin --delete <branch-name>
```

## 4. Clean Up Script

Here's a script to automate the cleanup process:

```bash
#!/bin/bash

# Switch to main and update
git checkout main
git pull origin main

# Get list of fully merged branches (excluding main)
merged_branches=$(git branch --merged | grep -v "main" | xargs)

# Delete local merged branches
for branch in $merged_branches; do
  echo "Deleting local branch: $branch"
  git branch -d $branch
done

# Delete remote branches that have been merged
for branch in $merged_branches; do
  echo "Deleting remote branch: $branch"
  git push origin --delete $branch
done

# Prune remote tracking branches that no longer exist on the remote
git fetch --prune

echo "Branch cleanup complete!"
```

## 5. Verify Clean State

After cleanup, verify that only necessary branches remain:

```bash
# Check remaining branches
git branch -a
```

This approach ensures that all branches are properly merged to main and that both local and remote branches are cleaned up afterward.