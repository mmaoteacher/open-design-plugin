---
name: setup
description: Configure or repair OpenDesign for Claude Code, Codex, or agy using an existing local Open Design.app installation. Use after installing this plugin or updating/moving the app, or when OpenDesign skills or MCP paths are missing.
---

# Set up local OpenDesign resources

Use the installed plugin root containing this SKILL.md (two directories above it).
Do not run a different development checkout: hosts load their installed copy, often
in a versioned cache. The public plugin includes only this skill. Setup links local
app resources; it does not download or redistribute OpenDesign content.

1. Select the current host: `--agent claude` (alias `cc`), `--agent codex`, or
   `--agent agy`. Ask which host only if the current environment is unclear.
2. Run `bash "<installed-plugin-root>/setup.sh" --agent <host> --dry-run`.
   Requires Python 3 and Node.js. Searches `/Applications/Open Design.app` then
   `~/Applications/Open Design.app`. For a custom installation use
   `--app "/path/to/Open Design.app"`. An explicit invalid path must fail.
3. If the app is absent, ask for its installed location or explain the prerequisite.
   Otherwise run the same command without `--dry-run`. Invoking this skill authorizes
   local plugin configuration. Preserve conflicting unmanaged or user-modified files;
   report the path instead of deleting them automatically.
4. Report the actual skill count and resource location. Ask the user to open Open
   Design.app, restart the selected CLI and begin a new session. Claude Code users
   may also use `/reload-plugins`. Codex loads new plugin skills in a new thread.
   If MCP tools are available, verify with a read-only call. File setup alone does
   not prove the app's daemon is reachable at `127.0.0.1:7456`.

Claude Code and Codex use the generated `.mcp.json`; agy uses `mcp_config.json`.
The generated `opendesign-systems` skill points to local design resources and the
UI/UX rules. Do not assume every host automatically loads `rules/AGENTS.md`.
No global CLI configuration, other plugins, or app files are modified.

Rerun setup after app upgrades, relocation, or plugin updates/reinstallation: a new
plugin cache initially has only setup again. It refreshes managed links and removes
obsolete skill links. Some bundled skills are upstream stubs; follow their own
instructions when used and do not claim their dependencies were downloaded.
Generated local files are ignored by Git; never force-add them to a publication.
