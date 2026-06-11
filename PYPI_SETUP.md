# PyPI Setup Guide for Edge Reader

This guide walks you through setting up automatic publishing to PyPI via GitHub Actions.

## Step 1: Create PyPI Account

1. Visit **https://pypi.org/account/register/**
2. Fill in the form:
   - Username: (your choice)
   - Email: (your email)
   - Password: (strong password)
3. Click **"Register"**
4. Verify your email address via the confirmation link

## Step 2: Enable 2FA (Recommended)

1. Log in to PyPI: **https://pypi.org/account/login/**
2. Go to **"Account Settings"** (top right, click your username)
3. Scroll to **"Two Factor Authentication"**
4. Click **"Add 2FA"**
5. Choose **"Authentication application"** (Google Authenticator, Authy, etc.)
6. Follow the setup instructions
7. Save your recovery codes in a safe place

## Step 3: Create API Token

1. Log in to PyPI
2. Go to **"Account Settings"** → **"API tokens"**
3. Click **"Add API token"**
4. Fill in:
   - Name: `github-actions-edge-reader`
   - Scope: **Entire account** (for first publish, safer to use specific project later)
5. Click **"Create token"**
6. **IMPORTANT: Copy the token immediately** (you won't see it again!)
   - Token format: `pypi-AgEIcHlwaS5...`

## Step 4: Add Secret to GitHub

### Via GitHub Web UI:

1. Go to **https://github.com/Monotoba/edge-reader/settings/secrets/actions**
2. Click **"New repository secret"**
3. Fill in:
   - **Name:** `PYPI_API_TOKEN`
   - **Secret:** Paste your PyPI token
4. Click **"Add secret"**

### Verify it was added:
- You should see `PYPI_API_TOKEN` listed (with value hidden)

## Step 5: Test the Automation (Optional)

### Method 1: Dry Run via GitHub Actions

1. Go to **https://github.com/Monotoba/edge-reader/actions**
2. Click **"Publish to PyPI"** workflow
3. Click **"Run workflow"** button
4. Select branch: `main`
5. Input: `Dry run: true`
6. Click **"Run workflow"**
7. Watch the workflow execute (click on it to see details)

### Method 2: Create a Test Release

1. Go to **https://github.com/Monotoba/edge-reader/releases**
2. Click **"Draft a new release"**
3. Fill in:
   - Tag version: `v0.1.0` (or next version)
   - Release title: `Release 0.1.0`
   - Description: `Initial release`
4. Check **"This is a pre-release"** (optional, for testing)
5. Click **"Publish release"**
6. Watch the workflow automatically trigger and publish!

## Publishing Process (Step-by-Step)

### Local Machine:

```bash
# 1. Update version
./scripts/version.sh

# 2. Commit and push
git add pyproject.toml
git commit -m "Bump version to X.Y.Z"
git push origin main
```

### GitHub:

```bash
# 3. Create release (this triggers auto-publish)
gh release create vX.Y.Z --title "Release X.Y.Z" --notes "See CHANGELOG"
# OR do it via web UI: https://github.com/Monotoba/edge-reader/releases/new
```

The GitHub Actions workflow will automatically:
1. Build the distribution (wheel + source)
2. Validate with twine
3. Publish to PyPI

## Verify Publication

After workflow completes:

```bash
# Check on PyPI
pip install edge-readaloud-pyside6

# Or visit:
# https://pypi.org/project/edge-readaloud-pyside6/
```

## Troubleshooting

### "Invalid API token"
- Verify you copied the entire token from PyPI
- Check it doesn't have extra spaces
- Regenerate if you're unsure

### "Workflow shows red X"
- Click the workflow run to see detailed error
- Common issues:
  - Token expired/invalid
  - Version already published
  - Build failed (check tests)

### "Token keeps expiring"
1. Create a new token on PyPI
2. Update the GitHub secret with new token
3. Old tokens remain valid until you revoke them

### "Want to publish a pre-release?"
- Use `--prerelease` flag:
  ```bash
  gh release create vX.Y.ZrcN --prerelease --title "X.Y.Z Release Candidate N"
  ```

## Multiple Environments

### Test PyPI (Optional)

For testing before real release:

1. Create account at **https://test.pypi.org/account/register/**
2. Create API token on Test PyPI
3. Create GitHub secret: `PYPI_API_TOKEN_TEST`
4. Create test workflow in `.github/workflows/publish-test.yml`

## Security Best Practices

- ✅ Use API tokens (not account password)
- ✅ Enable 2FA on PyPI account
- ✅ Use organization tokens if available
- ✅ Rotate tokens periodically
- ✅ Never commit tokens to git
- ✅ Keep recovery codes safe

## After Publishing

### Announce Release:

1. Create GitHub release notes
2. Update CHANGELOG.md
3. Tag release on GitHub
4. Consider posting on:
   - GitHub discussions
   - Python communities
   - Reddit r/Python
   - Your blog/website

### Monitor:

- Check PyPI for download stats
- Monitor GitHub issues
- Review user feedback

## Reference

- PyPI: https://pypi.org/
- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- twine: https://twine.readthedocs.io/
- GitHub Actions: https://docs.github.com/en/actions
