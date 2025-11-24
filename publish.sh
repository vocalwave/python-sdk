#!/bin/bash
# Publishing script for Python SDK

set -e

echo "🐍 Publishing QRNG Python SDK to PyPI"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from sdks/python directory"
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# Install build tools
echo "📦 Installing build tools..."
pip install --quiet --upgrade build twine

# Build the package
echo "🔨 Building package..."
python -m build

# Check the package
echo "✅ Checking package..."
twine check dist/*

# Ask for confirmation
echo ""
echo "📋 Package built successfully!"
echo "   Files: $(ls dist/)"
echo ""
read -p "Upload to TestPyPI first? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "⬆️  Uploading to TestPyPI..."
    twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Uploaded to TestPyPI!"
    echo "   Test install: pip install --index-url https://test.pypi.org/simple/ qrng-api"
    echo ""
    read -p "Continue to production PyPI? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborted"
        exit 0
    fi
fi

echo "⬆️  Uploading to PyPI..."
twine upload dist/*

echo ""
echo "✅ Successfully published to PyPI!"
echo "   Install: pip install qrng-api"
echo "   Verify: python -c 'from qrng import QRNGClient; print(QRNGClient)'"
