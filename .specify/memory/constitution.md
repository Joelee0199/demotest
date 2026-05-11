<!--
Sync Impact Report
==================
Version change: N/A → 1.0.0
Modified principles: (initial creation)
  - Principle 1: 代码简洁清晰 (new)
  - Principle 2: Python 3.11+ & Flask 技术栈 (new)
  - Principle 3: SQLite 单一数据存储 (new)
  - Principle 4: 密码哈希存储 (new)
  - Principle 5: 接口错误处理 (new)
  - Principle 6: 文件行数限制 (new)
Added sections: Purpose, Principles (1–6), Governance
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/constitution-template.md ✅ (source)
  - .specify/templates/plan-template.md ✅ created
  - .specify/templates/spec-template.md ✅ created
  - .specify/templates/tasks-template.md ✅ created
Follow-up TODOs: None
-->

# 个人博客 — Project Constitution

> Version 1.0.0 | Ratified 2026-05-08 | Last Amended 2026-05-08

## Purpose

本项目是一个基于 Python Flask 的个人博客系统，旨在提供一个轻量、
安全、易维护的内容发布平台。所有代码和架构决策必须服务于以下
六条核心原则，确保项目对新手友好、安全可靠且易于长期维护。

## Principles

### Principle 1: 代码简洁清晰

所有代码 MUST 保持简洁清晰，确保 Python 新手也能无障碍阅读
和理解。具体要求：

- 函数和变量命名 MUST 使用自描述的英文单词，避免晦涩缩写。
- 每个函数 MUST 只做一件事（单一职责）。
- 复杂逻辑 MUST 附带行内注释说明意图，而非仅描述"做了什么"。
- 禁止过度工程化：不得引入当前需求不需要的设计模式或抽象层。

**Rationale**: 个人博客的生命周期往往伴随维护者的更换或间歇性
开发。新手可读的代码大幅降低上手成本，减少因理解偏差引入的
回归缺陷。

### Principle 2: Python 3.11+ & Flask 技术栈

项目 MUST 使用 Python 3.11 或更高版本，并基于 Flask 框架
构建。具体约束：

- MUST 使用 Python 3.11+ 的语法特性（如 `match` 语句、
  `ExceptionGroup` 等），不得向后兼容旧版本。
- Web 框架 MUST 使用 Flask；不得引入 Django、FastAPI 或
  其他替代框架。
- 依赖管理 MUST 使用 `requirements.txt`，并锁定版本号
  （`package==x.y.z` 格式）。
- 第三方库的选择 MUST 优先考虑 Flask 生态兼容性。

**Rationale**: 统一技术栈减少认知负担，Flask 的微框架特性
契合"简洁清晰"原则，Python 3.11+ 提供更好的性能和语法糖。

### Principle 3: SQLite 单一数据存储

项目 MUST 使用 SQLite 作为唯一的数据存储方案。具体约束：

- 所有持久化数据 MUST 存储在 SQLite 数据库文件中。
- MUST NOT 引入任何外部数据库服务（如 MySQL、PostgreSQL、
  Redis、MongoDB）。
- 数据库访问 MUST 通过 Flask-SQLAlchemy 或原生 `sqlite3`
  模块，不得使用裸 SQL 拼接（参见安全原则）。
- 数据库迁移 MUST 使用 Flask-Migrate / Alembic 管理。

**Rationale**: 个人博客的并发量和数据规模远低于需要外部数据库
的阈值。SQLite 零配置、单文件部署的特性极大简化了开发、测试
和运维成本。

### Principle 4: 密码哈希存储

所有密码和敏感凭证 MUST 使用单向哈希存储，绝对禁止明文存储。
具体要求：

- 用户密码 MUST 使用 `werkzeug.security` 中的
  `generate_password_hash` / `check_password_hash`，或
  `bcrypt` / `argon2` 等业界公认的哈希算法。
- MUST NOT 在任何日志、数据库字段、配置文件中明文存储密码。
- API Key 等凭证 MUST 使用环境变量或密钥管理服务注入，
  MUST NOT 硬编码在源码中。
- 密码验证 MUST 使用常量时间比较函数，防止时序攻击。

**Rationale**: 密码明文存储是最高危的安全漏洞之一。一旦数据
泄露，明文密码将直接威胁用户在其他平台的账户安全。哈希存储
是最低限度的安全基线，不可妥协。

### Principle 5: 接口错误处理

所有对外接口（HTTP 端点、CLI 命令、内部服务调用）MUST
实现完善的错误处理。具体要求：

- 每个 Flask 路由 MUST 包含 `try/except` 或使用
  `@app.errorhandler` 注册全局异常处理器。
- 错误响应 MUST 返回合适的 HTTP 状态码和 JSON 格式的
  错误信息（含 `error` 字段和人类可读的 `message`）。
- MUST NOT 将 Python 原始异常堆栈暴露给前端用户（开发模式
  除外）。
- 数据库操作 MUST 处理 `IntegrityError`、`OperationalError`
  等常见异常。
- 外部调用（如文件 I/O、网络请求）MUST 处理超时和连接失败。

**Rationale**: 缺乏错误处理的接口不仅导致糟糕的用户体验，
还可能泄露内部实现细节，成为攻击者的信息来源。完善的错误
处理是稳定性和安全性的双重保障。

### Principle 6: 文件行数限制

每个 Python 源码文件 MUST NOT 超过 200 行（不含空行和纯
注释行）。具体约束：

- 当文件接近 200 行时，MUST 拆分为更小的模块或工具函数。
- 拆分 MUST 遵循功能内聚原则：相关的函数放在同一模块，
  不相关的逻辑分离到不同文件。
- 配置文件（`config.py`）、数据库模型文件（`models.py`）
  同样受此限制约束。
- 测试文件可适当放宽，但 SHOULD NOT 超过 300 行。

**Rationale**: 文件过长是代码腐化的首要征兆。200 行限制强制
开发者保持模块的单一职责，提升代码可导航性和可审查性，也
契合"简洁清晰"原则。

## Governance

### Amendment Procedure

1. 任何贡献者 MAY 通过提交 Pull Request 提出宪法修正案。
2. 修正案 MUST 至少由一名项目维护者审查通过。
3. 破坏性变更（原则删除或重新定义）递增 MAJOR 版本；
   新增原则或实质性扩展递增 MINOR 版本；文字澄清和
   措辞修正递增 PATCH 版本。

### Versioning Policy

本宪法遵循语义化版本控制。每次文档变更 MUST 伴随版本号递增，
并在文件顶部的 Sync Impact Report 中记录变更内容。

### Compliance Review

所有功能规格说明和实施计划 MUST 引用其所遵循的原则编号。
任何规格说明若与既有原则相矛盾，MUST 被驳回，或先正式
修正宪法后再行推进。
