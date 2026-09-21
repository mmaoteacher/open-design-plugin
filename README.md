# OpenDesign Plugin

讓 Claude Code（cc）、Codex 與 Antigravity（agy）使用本機 Open Design.app 的 skills、design systems、templates 與 MCP。
公開套件初始只有 `setup` skill，不收錄 OpenDesign 的原始內容；執行 setup 才產生本機連結與設定。
OpenCode 不在支援範圍。

## 前置需求

macOS、Python 3、Node.js，以及已安裝的 Open Design.app。

## 安裝與設定

以下遠端安裝方式需 repository 已包含本版本的 marketplace 與 manifest。
安裝後請在對應 CLI 執行本 plugin 的 setup skill，讓它在**實際安裝副本**中配置資源。

### Claude Code（cc）

在 Claude Code 中執行：

```text
/plugin marketplace add git@github.com:mmaoteacher/open-design-plugin.git
/plugin install open-design-plugin@open-design
/open-design-plugin:setup
```

Setup 使用 `--agent claude`（也接受 `--agent cc`），產生 `.mcp.json`。
完成後重新啟動 Claude Code 或執行 `/reload-plugins`。
本機開發也可用 `claude --plugin-dir /path/to/open-design-plugin` 載入 checkout。

### Codex

```bash
codex plugin marketplace add git@github.com:mmaoteacher/open-design-plugin.git
codex plugin add open-design-plugin@open-design
```

開啟新對話，請 Codex「執行 open-design-plugin 的 setup skill」。
Setup 使用 `--agent codex`，產生 `.mcp.json`。完成後重新啟動 Codex 並開新對話，載入新 skills 與 MCP。

### Antigravity（agy）

```bash
git clone https://github.com/mmaoteacher/open-design-plugin.git \
  ~/.gemini/config/plugins/open-design-plugin
```

重新啟動 agy，請 agent「執行 open-design-plugin 的 setup skill」。
Setup 使用 `--agent agy`，產生 `mcp_config.json`。
此專案使用 agy plugin 格式；未驗證原生 Gemini CLI extension 的安裝相容性。

### 手動 setup

請在 CLI **已載入的 plugin 根目錄**執行，不要誤用其他開發 checkout：

```bash
./setup.sh --agent codex --dry-run
./setup.sh --agent codex
# 其他 host：--agent claude、--agent cc、--agent agy
```

未指定 `--agent` 時預設 agy，以相容舊用法。可對同一副本依序指定多個 host，會保留先前已配置的 host。
Setup 搜尋 `/Applications/Open Design.app`，再搜尋 `~/Applications/Open Design.app`。
自訂位置可用：

```bash
./setup.sh --agent claude --app "/path/to/Open Design.app"
OPEN_DESIGN_APP_PATH="/path/to/Open Design.app" ./setup.sh --agent codex
```

明確指定的錯誤路徑會報錯，不會改用另一個 app。
MCP 運作時需開啟 Open Design.app，讓 daemon 在 `127.0.0.1:7456` 提供服務。

## 本機資源與更新

- 逐一連結 app 中含 `SKILL.md` 的 skill 資料夾，保留 scripts、references 與 assets。
- 連結 `design-systems`、`design-templates`，並產生本專案的 `opendesign-systems` 整合 skill。
- 產生 UI/UX 規則，透過整合 skill 明確引導讀取；不假設各 host 會自動載入 plugin 的 `rules/AGENTS.md`。
- MCP 使用找到的 Node.js 與 app 的固定 daemon 入口；舊版才尋找唯一的 `cli-*.mjs`。
- 重跑會更新連結、移除已消失的 skill 連結。遇到使用者修改或未管理的同名內容會停止並保留原檔。

不會下載或修改 app，也不改寫其他 plugins 或全域 CLI 設定。
部分 app skills 是上游入口，不代表其依賴已安裝；功能數量依本機 app 版本而定。

**App 更新、搬移，或 plugin 更新／重裝後，請重跑 setup。** CLI 可能建立新的版本 cache，
新的 cache 仍只包含 setup。應在新副本內配置，不要將舊副本連結或絕對路徑提交到遠端。
所有生成的 skills、資源連結、rules、MCP 設定與狀態記錄都由 `.gitignore` 排除，請勿 force-add。

## 開發與驗證

使用獨立 checkout，例如 `~/Documents/workspace/mmao/open-design-plugin`。
各 CLI 安裝副本留作執行用途；維護原則見 [AGENTS.md](AGENTS.md)。

```text
plugin.json                        # agy manifest
.codex-plugin/plugin.json          # Codex manifest
.agents/plugins/marketplace.json   # Codex marketplace
.claude-plugin/plugin.json         # Claude Code manifest
.claude-plugin/marketplace.json    # Claude Code marketplace
skills/setup/SKILL.md              # 初始唯一 skill
setup.sh                          # 共用入口
scripts/setup.py                  # 資源偵測與各 host 配置
templates/                       # 本專案整合 skill / 規則
tests/                           # 隔離測試
```

Marketplace 指向 repository 根目錄 `./`，讓三種 CLI 共用同一份 setup 與範本。

```bash
python3 -m unittest discover -s tests -v
agy plugin validate .
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

Codex 本機安裝測試可將此 checkout 加為 marketplace，再安裝；開發驗證建議使用隔離的 `CODEX_HOME`。
實際驗證結果與限制見 [tests/VALIDATION.md](tests/VALIDATION.md)。

格式參考：[Claude Code plugin 文件](https://code.claude.com/docs/en/plugins-reference)、
[Codex plugin 文件](https://developers.openai.com/plugins/build/plugins)。

## 從 1.x 升級

先備份自訂 skills、rules 與 MCP 配置，再更新 repository 並執行 setup。
若殘留未追蹤的同名目錄，先將該目錄移到備份位置再重跑。
移除目前版本的內容不會清除 Git 歷史中已提交的副本；本專案沒有重寫舊歷史。
