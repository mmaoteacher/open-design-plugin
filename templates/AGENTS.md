# OpenDesign UI/UX 規範與設計工程契約 (open-design-plugin)

本文件定義 Agent 在執行任何 UI/UX、前端元件設計與頁面重構時應遵循的高審美與工程規範。

## 1. 核心設計原則 (Anti-AI-Slop & High Agency)
在撰寫任何 UI 代碼（Astro, SolidJS, React, HTML/CSS）時，嚴格杜絕「廉價 AI 生成感」：
- **禁止無意義的 AI 俗套漸變**：杜絕濫用藍紫霓虹漸變（purple-blue gradient glow）或暗黑風背景配發光邊框，除非品牌設計規格明確要求。
- **杜絕模板化三卡片**：避免千篇一律的「頂部 Hero + 3 等分卡片 + 底座按鈕」版面，依據實際內容資訊架構調整版面佈局（Bento Grid、雜誌編排、高密度儀表板等）。
- **嚴謹的圓角與陰影層級**：避免全站滿版的大圓角（`rounded-3xl` 氾濫），採用符合專業軟體質感的微圓角與精緻陰影（subtle borders & multi-layered soft shadows）。
- **視覺密度與節奏**：行距、間距（Gap / Padding）必須有節奏感，避免大片空洞浪費或過度擁擠。

## 2. 本機 Design Systems 與 Tokens 存取
可用品牌設計系統依本機 Open Design.app 版本而定：
- **路徑**：`~/.gemini/config/plugins/open-design-plugin/design-systems/<brand>/`
- **品牌包含**：`apple` (HIG), `linear`, `airbnb`, `arc`, `binance`, `bmw`, `cal`, `bento`, `canva` 等。

## 3. 審查與打磨工作流 (Impeccable Polish)
在產出或修改前端 UI 後，必須進行自體審查：
1. **Hierarchy (層級)**：標題、副標、內文是否有清晰的字階與對比度？
2. **Accessibility (無障礙)**：按鈕與連結是否有 Focus 狀態？色彩對比是否達到 WCAG AA？
3. **Responsiveness (響應式)**：在行動端檢驗是否有水平溢出（overflow-x）、文字截斷或點擊熱區過小問題。
4. **Motion Discipline (動態紀律)**：微動畫必須服務於操作反饋或空間連續性，嚴禁無意義的晃動與旋轉。

## 4. OpenDesign 畫布連動 (MCP)
當本地 Open Design.app 開啟時，可透過 `open-design` MCP 工具（如 `create_artifact`, `get_artifact`）進行畫布與即時預覽連動。
