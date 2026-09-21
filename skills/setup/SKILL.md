---
name: setup
description: Configure or repair the OpenDesign plugin using an existing local Open Design.app installation. Use after installing this plugin or updating/moving the app, or when OpenDesign skills or MCP paths are missing.
---

# Set up local OpenDesign resources

Run `setup.sh` from this plugin's root (two directories above this SKILL.md).
The public plugin includes only this skill. Setup links the app's skills and design
resources and generates the plugin's integration skill, rules, and MCP configuration.
It does not download OpenDesign or copy its bundled content.

1. Run `bash "<plugin-root>/setup.sh" --dry-run` to discover and validate resources.
   Requires Python 3 and Node.js. Default app locations are `/Applications/Open Design.app`
   and `~/Applications/Open Design.app`.
2. If no app is found, ask for its installed location, or explain that the user must
   install Open Design first. Use `--app "/path/to/Open Design.app"` for a custom path.
   An explicitly supplied path must not silently fall back to another installation.
3. Run the same command without `--dry-run`. Running this skill authorizes the local
   configuration. If an existing unmanaged or modified file conflicts, report its
   path and preserve it; do not delete it automatically.
4. Report the actual skill count and resource location. Ask the user to open Open
   Design.app and restart agy so it reloads plugin skills and MCP. If MCP tools are
   available after reload, use a read-only call to verify connectivity; filesystem
   setup alone does not establish that the running app is reachable.

Rerun setup after app upgrades or relocation. It refreshes managed links and removes
obsolete managed skill links. Some app-bundled skills are upstream stubs: follow their
instructions when used; do not claim setup downloaded their upstream dependencies.
Generated files are ignored by Git. Never add them or app resources to a publication.
