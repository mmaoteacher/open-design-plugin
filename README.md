# OpenDesign Plugin (for Antigravity / Gemini CLI)

OpenDesign UI/UX 迭代強化器外掛，整合 150+ 專業設計 Skills、154 套品牌 Design Systems（含 Tailwind v4 CSS Tokens）、OpenDesign 本地 MCP 工具集，以及反 AI 俗套（Anti-AI-Slop）高審美前端工程規範。

---

## 📦 核心內容

1. **150+ 專業設計 Skills (`skills/`)**：
   - 涵蓋簡報演講（`ppt-keynote`, `slides`, `deck-*`）、海報雜誌（`article-magazine`, `poster-hero`）、動態動畫（`gsap-*`, `emilkowalski-motion`, `remotion`）、向量與 3D 視覺（`threejs`, `shader-dev`, `hand-drawn-diagrams`）等。
2. **154 套品牌 Design Systems (`design-systems/`)**：
   - Apple HIG, Linear, Airbnb, Arc, Cal, Bento, Stripe, BMW 等品牌 Tokens 與設計系統連結。
3. **OpenDesign MCP Server (`mcp_config.json`)**：
   - 與本機 Open Design.app 畫布即時連動，支援 `create_artifact`, `get_artifact`, `start_run` 等工具。
4. **高審美 UI/UX 規範契約 (`rules/AGENTS.md`)**：
   - 強制約束視覺階層（Hierarchy）、無障礙（Accessibility）、響應式（Responsiveness）與動態紀律（Motion Discipline）。

---

## 🚀 跨機器快速複製配置 (Quick Setup)

在任何新機器上，只需執行以下步驟即可快速完成配置：

### 1. 前置需求 (Prerequisites)
- **macOS**
- **Node.js**（MCP Server 執行環境）
- **Open Design.app**（預設安裝於 `/Applications/Open Design.app`）
- **Antigravity / Gemini CLI**

### 2. 一鍵 Clone 與初始化 (One-Line Setup)

打開終端機執行：

```bash
# 確保 plugins 目錄存在，並 Clone 儲存庫
mkdir -p ~/.gemini/config/plugins
git clone git@github.com:mmaoteacher/open-design-plugin.git ~/.gemini/config/plugins/open-design-plugin

# 執行初始化健康檢查與軟連結建立
cd ~/.gemini/config/plugins/open-design-plugin
./setup.sh
```

> **提示**：若使用 HTTPS，請將 clone 網址改為：  
> `git clone https://github.com/mmaoteacher/open-design-plugin.git ~/.gemini/config/plugins/open-design-plugin`

### 3. 自訂 Open Design.app 路徑（非預設安裝位置時）
若 Open Design.app 安裝於其他路徑，可指定環境變數執行 `setup.sh`：
```bash
OPEN_DESIGN_APP_PATH="/path/to/Open Design.app" ./setup.sh
```

---

## ⚙️ 專案結構

```
open-design-plugin/
├── plugin.json         # 外掛描述與版本資訊
├── mcp_config.json      # OpenDesign MCP 伺服器啟動配置
├── setup.sh            # 跨機器一鍵檢查與符號連結修復腳本
├── rules/
│   └── AGENTS.md       # OpenDesign UI/UX 規範與設計工程契約
├── skills/             # 150+ 模組化設計技能目錄
├── design-systems      # 符號連結 -> Open Design.app 內建 154 套品牌系統
└── design-templates    # 符號連結 -> Open Design.app 內建模板資源
```

---

## 🔄 日常維護與同步

- **拉取最新配置**：
  ```bash
  cd ~/.gemini/config/plugins/open-design-plugin
  git pull
  ```
- **提交本地修改**：
  ```bash
  cd ~/.gemini/config/plugins/open-design-plugin
  git add .
  git commit -m "feat(skills): update custom skills"
  git push
  ```
