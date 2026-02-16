#!/usr/bin/env bash
# Dictate — One-liner setup script for macOS
set -euo pipefail

echo "=== Dictate Setup ==="

# Check macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "Error: Dictate only runs on macOS."
    exit 1
fi

# Check Python version
PYTHON_CMD=""
for cmd in python3.12 python3.11 python3.10 python3; do
    if command -v "$cmd" &>/dev/null; then
        version=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        major=$("$cmd" -c "import sys; print(sys.version_info.major)")
        minor=$("$cmd" -c "import sys; print(sys.version_info.minor)")
        if [[ "$major" -eq 3 ]] && [[ "$minor" -ge 10 ]] && [[ "$minor" -le 13 ]]; then
            PYTHON_CMD="$cmd"
            echo "Using Python $version ($cmd)"
            break
        fi
    fi
done

if [[ -z "$PYTHON_CMD" ]]; then
    echo "Error: Python 3.10–3.13 is required."
    echo "Install with: brew install python@3.12"
    exit 1
fi

# Create virtual environment
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"

if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtual environment..."
    "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -e "$PROJECT_DIR"

# Copy .env if not exists
if [[ ! -f "$PROJECT_DIR/.env" ]]; then
    cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
    echo "Created .env from .env.example — edit as needed."
fi

echo ""
echo "=== Setup complete! ==="
echo ""
echo "To start Dictate:"
echo "  source $VENV_DIR/bin/activate"
echo "  python -m dictate"
echo ""
echo "Required macOS permissions:"
echo "  1. Microphone — will be prompted automatically"
echo "  2. Accessibility — grant manually in:"
echo "     System Settings → Privacy & Security → Accessibility"
echo "     Add your terminal app (Terminal.app, iTerm, etc.)"
