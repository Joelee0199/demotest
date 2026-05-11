# Spec: [FEATURE_NAME]

> Created: [DATE] | Status: DRAFT | Constitution Version: 1.0.0

## Summary

[One-paragraph description of the feature.]

## Constitutional Principles

List the principles this spec adheres to:

- **P1 代码简洁清晰**: [How this spec upholds P1]
- **P2 Python 3.11+ & Flask**: [Tech stack alignment]
- **P3 SQLite 单一数据存储**: [Data storage approach]
- **P4 密码哈希存储**: [Security considerations]
- **P5 接口错误处理**: [Error handling strategy]
- **P6 文件行数限制**: [File structure plan]

> If any principle is violated, the spec MUST be rejected or the
> constitution MUST be formally amended first.

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | [Description] | Must/Should/May |

### Non-Functional Requirements

| ID | Requirement | Principle |
|----|-------------|-----------|
| NFR-001 | [Description] | [P1–P6] |

## API Design

### Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /api/[resource] | [Description] | Yes/No |

### Error Responses

All endpoints MUST return errors in the following format (P5):

```json
{
  "error": "NOT_FOUND",
  "message": "Human-readable description"
}
```

## Data Model

All data MUST be stored in SQLite (P3).

| Table | Fields | Constraints |
|-------|--------|-------------|
| [name] | [fields] | [constraints] |

## File Structure

Each file MUST NOT exceed 200 lines (P6).

```
app/
├── __init__.py
├── routes/
│   └── [feature].py
├── models/
│   └── [feature].py
└── services/
    └── [feature].py
```
