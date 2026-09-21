# OpenDesign Plugin（agy / Antigravity）

讓 agy 使用本機 Open Design.app 的 skills、design systems、templates 與 MCP。
此 repository 只提供 setup skill 與整合程式，不收錄 OpenDesign 的原始 skills 或設計資源。

## 安裝

需要 macOS、Python 3、Node.js，以及已安裝的 Open Design.app。

```bash
git clone https://github.com/mmaoteacher/open-design-plugin.git \
  ~/.gemini/config/plugins/open-design-plugin
```

重新啟動 agy，請 agent「執行 open-design-plugin 的 setup skill」。
首次安裝只會發現 `setup`，尚未註冊 OpenDesign MCP。
也可以直接執行：

```bash
cd ~/.gemini/config/plugins/open-design-plugin
./setup.sh --dry-run
./setup.sh
```

Setup 會依序搜尋 `/Applications/Open Design.app`、`~/Applications/Open Design.app`。
自訂位置可使用以下任一方式，明確指定的錯誤路徑會報錯：

```bash
./setup.sh --app "/path/to/Open Design.app"
OPEN_DESIGN_APP_PATH="/path/to/Open Design.app" ./setup.sh
```

完成後開啟 Open Design.app，並重新啟動 agy 載入新增 skills 與 MCP。
Setup 驗證本機檔案與配置；MCP 連線需 app 的 daemon 在 `127.0.0.1:7456` 運作。
此專案使用 agy plugin 格式；未驗證原生 Gemini CLI extension 安裝相容性。

## Setup 做了什麼

- 將 app 內含 `SKILL.md` 的 skill 資料夾逐一連結到 `skills/`，保留旁邊的 scripts、references 與 assets。
- 連結 `design-systems`、`design-templates` 至 app 本機資源。
- 產生本專案的 `opendesign-systems` 整合 skill 與 UI/UX 規則。
- 以找到的 Node.js 與 app daemon 入口產生 `mcp_config.json`；優先使用固定入口，舊版才尋找唯一的 `cli-*.mjs`。
- 記錄已管理的檔案；重跑會更新連結、移除已消失的 skill 連結。遇到使用者修改或未管理的同名內容會停止並保留原檔。

不會下載或修改 app，也不會刪除其他 plugin。功能數量依本機 app 版本而定；部分內建 skills 是上游入口，依其說明使用，不代表上游依賴已安裝。
App 更新或搬移後請重跑 setup。連結的內容會隨本機 app 更新。

## Repository 結構

```text
plugin.json               # 公開 plugin metadata
skills/setup/SKILL.md      # 初始唯一 skill
setup.sh                  # setup 入口
scripts/setup.py          # 本機偵測、驗證及配置
templates/               # 本專案整合 skill / 規則範本
tests/                   # 隔離的 setup 行為測試
```

Setup 產生的 skills 連結、資源連結、rules、MCP 配置與狀態記錄都在 `.gitignore` 中。
請勿使用 `git add -f` 將它們加入 repository。

## 從 1.x 升級

先備份自行修改的 skills、rules 與 MCP 配置，再更新 repository。
舊版本追蹤的 OpenDesign 內容在 2.x 移除，更新後執行 setup 即可重建本地整合。
若殘留未追蹤的同名目錄，setup 會指出衝突；先將該目錄移到備份位置，再重跑。

移除目前版本的檔案不會清除 Git 歷史中已提交的內容。若要連歷史也不含原始內容，
需另外建立乾淨歷史或新 repository；此變更不重寫歷史。

## 開發驗證

```bash
python3 -m unittest discover -s tests -v
agy plugin validate .
```
