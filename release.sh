#!/bin/env bash

set -e

if [[ -z "$VIRTUAL_ENV" ]]; then
    source venv/Scripts/activate
fi

# DONE - Fetch tags and get the latest one
git fetch --tags
version=$(git describe --tags $(git rev-list --tags --max-count=1))
version_number="${version#v}"  # Remove 'v' prefix if the tag has it
echo "Version: $version_number"

# Extract major, minor, and patch versions
IFS='.' read -r MAJOR_VERSION MINOR_VERSION PATCH_VERSION <<< "$version_number"
export MAJOR_VERSION MINOR_VERSION PATCH_VERSION
echo "Major version: $MAJOR_VERSION"
echo "Minor version: $MINOR_VERSION"
echo "Patch version: $PATCH_VERSION"

# Write version file
envsubst < version_file.txt > version_file.tmp
mv version_file.tmp version_file.txt
cat version_file.txt

# Install dependencies
pip install -r requirements.txt

# Lint with pylint
#pylint img2csv.py

# Test with pytest
#pytest test_img2csv.py

# Build executable with pyinstaller
pyinstaller --icon img2csv.ico --version-file version_file.txt --onefile img2csv.py

# Restore files with sensible data
cp img2csv.conf img2csv.conf.bak
git restore img2csv.conf

# Compress executable and related files
zip -j dist/img2csv.zip dist/img2csv.exe img2csv.conf
zip -r dist/img2csv.zip tess docs

# Write release notes
envsubst < release_notes.md > release_notes.tmp
mv release_notes.tmp release_notes.md
cat release_notes.md

# Create a release on GitHub
gh release create $version --verify-tag --notes-file release_notes.md --title "img2csv ${version} release" dist/img2csv.zip#img2csv.zip

# Reverting placeholder files
git restore release_notes.md
git restore version_file.txt
