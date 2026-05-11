# Tasks: [FEATURE_NAME]

> Created: [DATE] | Constitution Version: 1.0.0

## Task Categories

Tasks are categorized by constitutional principle to ensure compliance.

### P1 — 代码简洁清晰

| ID | Task | Est. | Status |
|----|------|------|--------|
| T-001 | [Description] | [1–8h] | ☐ |

### P2 — Python 3.11+ & Flask

| ID | Task | Est. | Status |
|----|------|------|--------|
| T-010 | [Description] | [1–8h] | ☐ |

### P3 — SQLite 单一数据存储

| ID | Task | Est. | Status |
|----|------|------|--------|
| T-020 | [Description] | [1–8h] | ☐ |

### P4 — 密码哈希存储

| ID | Task | Est. | Status |
|----|------|------|--------|
| T-030 | [Description] | [1–8h] | ☐ |

### P5 — 接口错误处理

| ID | Task | Est. | Status |
|----|------|------|--------|
| T-040 | [Description] | [1–8h] | ☐ |

### P6 — 文件行数限制

| ID | Task | Est. | Status |
|----|------|------|--------|
| T-050 | [Description] | [1–8h] | ☐ |

## Task Dependencies

```
T-001 → T-010 → T-020
                  ↓
T-030 ───────→ T-040 → T-050
```

## Completion Criteria

All tasks MUST:
- Pass linting and type checks (P1, P2)
- Not exceed 200 lines per file (P6)
- Include error handling in every endpoint (P5)
- Store passwords only as hashes (P4)
- Use SQLite exclusively for persistence (P3)
