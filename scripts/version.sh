#!/bin/bash
# Version update script for semantic versioning

set -e

# Get current version
CURRENT=$(grep 'version = ' pyproject.toml | head -1 | sed 's/.*version = "\(.*\)".*/\1/')

echo "Current version: $CURRENT"
echo ""
echo "Options:"
echo "1) Patch version (bug fixes) - $CURRENT → ${CURRENT%.*}.$((${CURRENT##*.}+1))"
echo "2) Minor version (features) - ${CURRENT%.*} → $((${CURRENT%.*%.*})).$((${CURRENT#*.} + 1)).0"
echo "3) Major version (breaking) - ${CURRENT%%.*} → $((${CURRENT%%.*}+1)).0.0"
echo "4) Custom version"
echo ""
read -p "Select option (1-4): " option

case $option in
    1)
        NEW_VERSION="${CURRENT%.*}.$((${CURRENT##*.}+1))"
        ;;
    2)
        MAJOR="${CURRENT%.*%.*}"
        MINOR="${CURRENT#*.}"
        NEW_VERSION="$MAJOR.$((MINOR+1)).0"
        ;;
    3)
        MAJOR="${CURRENT%%.*}"
        NEW_VERSION="$((MAJOR+1)).0.0"
        ;;
    4)
        read -p "Enter new version: " NEW_VERSION
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "Updating version: $CURRENT → $NEW_VERSION"
echo ""

# Update pyproject.toml
sed -i "s/version = \"$CURRENT\"/version = \"$NEW_VERSION\"/g" pyproject.toml

# Create git tag
read -p "Create git commit and tag? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add pyproject.toml
    git commit -m "Bump version to $NEW_VERSION"
    git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
    echo "✅ Git commit and tag created"
fi

echo ""
echo "✅ Version updated to $NEW_VERSION"
echo ""
echo "Next steps:"
echo "1. git push origin main"
echo "2. git push origin v$NEW_VERSION"
echo "3. ./scripts/build.sh"
echo "4. ./scripts/publish.sh"
