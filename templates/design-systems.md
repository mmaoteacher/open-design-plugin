---
name: opendesign-systems
description: |
  Search, inspect, and apply locally installed OpenDesign Design Systems (including Apple HIG, Linear, Airbnb, Arc, Cal, Bento, Stripe, BMW, etc.) with pre-compiled Tailwind CSS v4 tokens, CSS variables, and design guidelines.
triggers:
  - "design system"
  - "design tokens"
  - "tailwind tokens"
  - "apple hig tokens"
  - "linear design"
  - "airbnb design"
  - "bento grid"
  - "套用設計系統"
  - "設計風格"
  - "品牌設計"
---

# OpenDesign Design Systems Access Skill

此 Skill 讓 Agent 能夠直接檢索並套用 OpenDesign 本機版本提供的品牌與風格設計系統。

## 資源目錄位置
設計系統庫位於：
`~/.gemini/config/plugins/open-design-plugin/design-systems/`

## 常用核心品牌庫推薦
- `apple`: Apple Human Interface Guidelines (含繁中 DESIGN-zh-tw.md、iOS/macOS 精緻質感)
- `linear`: 現代深色高密度生產力工具美學
- `airbnb`: 溫暖、清晰、大間距與高無障礙標準
- `arc`: 漸變色調、個人化與瀏覽器級沉浸感
- `cal`: 現代排程工具的極簡與高效
- `bento`: Bento Grid 模組化佈局專用系統
- `brutalism`: 新野獸派風格
- `atelier-zero`: 極簡黑白排版風

## 每個設計系統的關鍵檔案
- `tailwind-v4.css`: 直接相容 Tailwind CSS v4 的 `@theme` 變數定義，可直接複製到專案的 CSS 入口。
- `tokens.css`: 基礎 CSS 自訂屬性（Custom Properties）。
- `design-tokens.json`: 原始 JSON 格式色票與字階。
- `DESIGN.md` / `DESIGN-zh-tw.md`: 核心設計理念與排版規則。

## 執行流程
1. 根據使用者的風格訴求，讀取目標品牌資料夾中的 `tailwind-v4.css` 或 `tokens.css`。
2. 將對應的 color palette、radius、font scale 等 tokens 映射至專案的 Tailwind 或元件樣式。
3. 遵循對應的 `DESIGN.md` 規範撰寫高水準的前端元件。

## UI/UX 整合規則

進行設計工作時，先讀取本 plugin 的 `../../rules/AGENTS.md`，再選擇設計系統。
此路徑相對於本 SKILL.md 所在資料夾；不要假設 host 會自動載入 plugin 的 rules 目錄。
