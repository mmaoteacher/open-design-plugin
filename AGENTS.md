# 維護指引

## 目標與支援範圍

本專案將本機 Open Design.app 資源整合至三種 CLI agent：

- Claude Code（cc）
- Codex
- Antigravity（agy）

OpenCode 不在支援範圍。現在已實作及驗證 agy；cc 與 Codex 的相容入口、安裝流程及載入驗證仍待實作。
不要將規劃中的平台標示為已支援。

## 維護與安裝分離

以這個 repository checkout 作為開發來源。各 CLI 的 plugin 安裝／cache 目錄是執行用副本，
不直接當作開發來源，也不因修改本專案而自動覆寫既有安裝。

## 共用設計

- 公開套件初始只暴露 setup skill；執行 setup 後才配置本機設計 skills、資源與 MCP。
- 不收錄或下載 OpenDesign 原始內容；連結使用者已安裝的 app 資源。
- 共用本機資源偵測與驗證邏輯，各平台的 manifest、MCP 格式與載入流程分開處理。
- 維持 setup 可重跑，保護未管理或經使用者修改的檔案。
- 本機生成的連結、設定與狀態必須留在 Git 追蹤範圍之外。
- 平台相容性需檢查實際 CLI 或官方規格，特別注意 plugin cache、符號連結與重新載入行為。

## 驗證

setup 邏輯變更執行 `python3 -m unittest discover -s tests -v`。
agy 格式可用 `agy plugin validate .` 驗證。
新增 cc／Codex 支援時，分別驗證初始僅有 setup、setup 後 skills／MCP 載入及重跑行為；
涉及使用者安裝的操作，先以隔離目錄測試。無法實測的部分需明確記錄。
