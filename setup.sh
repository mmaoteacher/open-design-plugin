#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME/.gemini/config/plugins/open-design-plugin"

echo "=== OpenDesign Plugin Setup ==="

# 1. Check if located in target plugins directory
if [ "$SCRIPT_DIR" != "$TARGET_DIR" ]; then
  echo "Current directory: $SCRIPT_DIR"
  echo "Target directory:  $TARGET_DIR"
  mkdir -p "$HOME/.gemini/config/plugins"
  if [ -e "$TARGET_DIR" ] && [ ! -L "$TARGET_DIR" ]; then
    echo "Warning: $TARGET_DIR already exists and is not a symlink."
    printf "Overwrite / link anyway? (y/N): "
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
      rm -rf "$TARGET_DIR"
      ln -s "$SCRIPT_DIR" "$TARGET_DIR"
      echo "Linked $SCRIPT_DIR -> $TARGET_DIR"
    fi
  elif [ ! -e "$TARGET_DIR" ]; then
    ln -s "$SCRIPT_DIR" "$TARGET_DIR"
    echo "Created symlink: $SCRIPT_DIR -> $TARGET_DIR"
  else
    echo "Symlink already exists at $TARGET_DIR"
  fi
fi

# 2. Check Open Design.app location
APP_PATH="${OPEN_DESIGN_APP_PATH:-/Applications/Open Design.app}"
if [ ! -d "$APP_PATH" ]; then
  if [ -d "$HOME/Applications/Open Design.app" ]; then
    APP_PATH="$HOME/Applications/Open Design.app"
  fi
fi

if [ ! -d "$APP_PATH" ]; then
  echo "⚠️ Warning: Open Design.app not found at /Applications or ~/Applications."
  echo "   If it is installed in another location, export OPEN_DESIGN_APP_PATH='/path/to/Open Design.app' and rerun."
else
  echo "✓ Found Open Design.app at: $APP_PATH"

  # 3. Verify / fix symlinks for design-systems and design-templates
  RESOURCES_DIR="$APP_PATH/Contents/Resources/open-design"
  if [ -d "$RESOURCES_DIR" ]; then
    cd "$SCRIPT_DIR"
    if [ ! -e "design-systems" ] || [ ! -L "design-systems" ]; then
      rm -rf design-systems
      ln -s "$RESOURCES_DIR/design-systems" design-systems
      echo "✓ Linked design-systems -> $RESOURCES_DIR/design-systems"
    else
      echo "✓ Symlink design-systems is present"
    fi

    if [ ! -e "design-templates" ] || [ ! -L "design-templates" ]; then
      rm -rf design-templates
      ln -s "$RESOURCES_DIR/design-templates" design-templates
      echo "✓ Linked design-templates -> $RESOURCES_DIR/design-templates"
    else
      echo "✓ Symlink design-templates is present"
    fi
  fi

  # 4. Check & update mcp_config.json daemon chunk path if necessary
  CHUNKS_DIR="$APP_PATH/Contents/Resources/app/prebundled/daemon/chunks"
  if [ -d "$CHUNKS_DIR" ]; then
    DAEMON_CLI=$(find "$CHUNKS_DIR" -name "cli-*.mjs" 2>/dev/null | head -n 1)
    if [ -n "$DAEMON_CLI" ]; then
      echo "✓ Found daemon CLI: $DAEMON_CLI"
      if [ -f "$SCRIPT_DIR/mcp_config.json" ]; then
        CURRENT_CLI=$(grep -oE '/Applications/Open Design\.app/Contents/Resources/app/prebundled/daemon/chunks/cli-[^"]+\.mjs' "$SCRIPT_DIR/mcp_config.json" 2>/dev/null || true)
        if [ -n "$CURRENT_CLI" ] && [ "$CURRENT_CLI" != "$DAEMON_CLI" ]; then
          echo "Updating mcp_config.json with new daemon chunk path..."
          sed -i '' "s|$CURRENT_CLI|$DAEMON_CLI|g" "$SCRIPT_DIR/mcp_config.json"
        fi
      fi
    fi
  fi
fi

# 5. Check Node.js
if command -v node >/dev/null 2>&1; then
  echo "✓ Node.js is installed ($(node -v))"
else
  echo "⚠️ Warning: 'node' command not found in PATH. MCP server requires Node.js."
fi

echo "=== OpenDesign Plugin configuration complete! ==="
