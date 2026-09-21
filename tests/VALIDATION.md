# CLI 支援驗證

日期：2026-09-21。環境：macOS、本機 Open Design.app、Node.js 22.23.1、Python 3。

| 項目 | 結果 |
| --- | --- |
| 14 項 setup 單元測試 | 通過；涵蓋兩種 MCP 格式、多 host 保留、舊狀態遷移、重跑、搬移、衝突保護及失敗前不寫入 |
| Codex CLI 0.155.0 | 隔離 marketplace 安裝；初始只有 setup、無 MCP；setup 後載入 159 skills、1 個 MCP 並成功取得工具清單 |
| Claude Code 2.1.278 | manifest／marketplace 驗證；隔離 marketplace 安裝；初始只有 setup、無 MCP；setup 後載入 159 skills、1 個 connected MCP |
| agy | 初始 1 skill、無 MCP；配置後 159 skills、1 MCP；既有預設入口保持相容 |
| 公開內容檢查 | 隔離副本執行三種 host setup 後 `git add .`，僅 setup skill 被追蹤，生成的 skills／資源／MCP／規則／狀態都未加入 |
| Codex manifest、setup skill 格式 | plugin-creator 與 skill-creator validator 通過 |

Claude Code 透過固定版本 npm 套件執行，不做全域安裝。CLI 測試使用暫存 `CODEX_HOME` 或
`CLAUDE_CONFIG_DIR`；沒有修改日常 CLI 設定。MCP 驗證只初始化連線／取得工具列表，未執行模型回合或寫入 artifact。

## 重現

```bash
python3 -m unittest discover -s tests -v
python3 tests/check_cli.py --agent codex
python3 tests/check_cli.py --agent claude --cli /path/to/claude
```

`check_cli.py` 需要對應 CLI、Node.js 及本機 Open Design.app，可使用 `--app` 指定 app。
它會建立、配置及清除隔離安裝。Claude Code 本機 marketplace 的來源目錄直接載入行為以 2.1.278 驗證；
Codex 使用實際安裝回傳的 cache 路徑。測試只檢查本 plugin 的 skills 與 MCP。

## 限制

- 計數取決於 app 版本；本次 app 提供 157 個 skills，加上 setup 與 opendesign-systems 共 159 個。
- 驗證的是 plugin 安裝、探索與 MCP 握手，不是每個上游 skill 的工作流或依賴。
- 此次透過隔離的本機 marketplace 測試；本次修改發布後，才可由 GitHub 安裝此版本。
- CLI 更新／重裝可能更換 cache；新副本需重新執行 setup。setup 應以目前載入的 SKILL.md 路徑定位 root。
