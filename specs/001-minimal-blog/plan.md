# Plan: Minimal Blog — Implementation

> Created: 2026-05-08 | Status: DRAFT | Constitution Version: 1.0.0

## Objective

实现一个极简个人博客系统，包含用户注册/登录/退出、文章发布/浏览/软删除
等核心功能。采用 Flask + SQLAlchemy + Jinja2 服务端渲染方案，
`python app.py` 即可本地运行。本计划严格遵循项目宪法六条原则，
按四个里程碑逐步交付。

## Constitutional Alignment

| Principle | Compliance |
|-----------|-----------|
| P1 代码简洁清晰 | ✅ 每个函数单一职责，命名自描述，无过度工程 |
| P2 Python 3.11+ & Flask | ✅ Flask + Flask-Login，无其他框架 |
| P3 SQLite 单一数据存储 | ✅ SQLAlchemy + SQLite，单文件数据库 |
| P4 密码哈希存储 | ✅ werkzeug.security 哈希存储，禁止明文 |
| P5 接口错误处理 | ✅ 全局错误处理器 + try/except + flash 消息 |
| P6 文件行数限制 | ✅ 路由按域拆分，每文件不超过 200 行 |

## Scope

### In Scope

- 项目脚手架：Flask app factory、配置、数据库初始化
- 用户模型与认证：注册、登录、退出（Flask-Login）
- 文章模型与 CRUD：创建、列表、详情、软删除
- 服务端渲染模板：6 个 HTML 页面（Jinja2）
- 表单验证与错误处理：flash 消息 + 全局异常捕获
- 入口脚本：`python app.py` 一键启动

### Out of Scope

- 文章编辑功能
- 分页
- 富文本 / Markdown 渲染
- 邮箱验证
- 管理后台 / 角色权限
- Docker 部署
- 前后端分离 / REST API
- 前端 CSS 框架（仅用极简内联样式）

## Technical Architecture

### Tech Stack

| Layer        | Choice                  | Rationale |
|--------------|-------------------------|-----------|
| Runtime      | Python 3.11+            | 宪法 P2 强制要求 |
| Framework    | Flask                   | 宪法 P2，微框架契合极简目标 |
| Auth         | Flask-Login             | 用户指定，标准 session 管理 |
| ORM          | Flask-SQLAlchemy        | 用户指定，防 SQL 注入 (P3, P5) |
| Password     | werkzeug.security       | 用户指定，宪法 P4 推荐方案 |
| Templates    | Jinja2 (Flask 内置)      | 用户指定，服务端渲染 |
| Database     | SQLite                  | 宪法 P3，零配置单文件 |
| Entry Point  | `python app.py`         | 用户指定，无 Docker |

### Dependencies (requirements.txt)

```
Flask==3.1.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
```

### Data Model

**User 表**

| Column        | Type      | Constraints          |
|---------------|-----------|----------------------|
| id            | INTEGER   | PK, AUTOINCREMENT    |
| email         | TEXT      | UNIQUE, NOT NULL     |
| password_hash | TEXT      | NOT NULL             |
| created_at    | DATETIME  | NOT NULL, default now|

**Post 表**

| Column     | Type      | Constraints              |
|------------|-----------|--------------------------|
| id         | INTEGER   | PK, AUTOINCREMENT        |
| title      | TEXT      | NOT NULL                 |
| body       | TEXT      | NOT NULL                 |
| author_id  | INTEGER   | FK → user.id, NOT NULL   |
| is_deleted | INTEGER   | NOT NULL, default 0      |
| created_at | DATETIME  | NOT NULL, default now     |

### File Structure

```
app/
├── __init__.py       # create_app() 工厂函数，注册扩展和蓝图
├── config.py          # Config 类：SQLALCHEMY_DATABASE_URI, SECRET_KEY
├── extensions.py      # db, login_manager 实例化（避免循环导入）
├── models.py          # User, Post 模型定义
├── routes/
│   ├── __init__.py    # 注册蓝图
│   ├── auth.py        # /login, /register, /logout
│   └── posts.py       # /, /post/<id>, /post/new, /post/<id>/delete
├── templates/
│   ├── base.html      # 基础布局 + 导航栏
│   ├── index.html     # 文章列表
│   ├── login.html     # 登录表单
│   ├── register.html  # 注册表单
│   ├── post_detail.html # 文章详情
│   └── post_new.html  # 发表文章表单
app.py                 # 入口：python app.py
requirements.txt
```

### Request Flow

```
浏览器请求 → Flask 路由 → 认证检查(login_required) → 业务逻辑 → 模板渲染 → HTML 响应
```

## Milestones

| # | Milestone | Target Date | Deliverables |
|---|-----------|-------------|--------------|
| 1 | 项目脚手架 + 数据模型 | Day 1 | `app/__init__.py`, `config.py`, `extensions.py`, `models.py`, `app.py`, `requirements.txt` |
| 2 | 用户认证（注册/登录/退出） | Day 2 | `routes/auth.py`, `templates/login.html`, `templates/register.html` |
| 3 | 文章功能（列表/详情/创建/删除） | Day 3 | `routes/posts.py`, `templates/index.html`, `templates/post_detail.html`, `templates/post_new.html` |
| 4 | 错误处理 + 模板完善 + 集成验证 | Day 4 | `templates/base.html`, 全局错误处理, 端到端流程验证 |

### Milestone 1: 项目脚手架 + 数据模型

**目标**: 搭建可运行的项目骨架，数据库表可自动创建。

**任务清单**:

1. 创建 `requirements.txt` 并锁定依赖版本
2. 创建 `app/config.py` — Config 类
   - `SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'`
   - `SECRET_KEY` 从环境变量读取，默认开发值
3. 创建 `app/extensions.py` — 实例化 `db` 和 `login_manager`
   - 避免循环导入：扩展在此初始化，在 `__init__.py` 中 `init_app()`
4. 创建 `app/models.py` — User 和 Post 模型
   - User: 继承 `UserMixin`，实现 `get_id()` 方法
   - Post: `is_deleted` 默认为 0，查询时过滤
   - User-Post: 一对多关系 `db.relationship('Post', backref='author')`
5. 创建 `app/__init__.py` — `create_app()` 工厂函数
   - 加载配置、初始化扩展、注册蓝图、创建数据表
6. 创建 `app/routes/__init__.py` — 蓝图注册辅助
7. 创建 `app/routes/auth.py` — 占位路由
8. 创建 `app/routes/posts.py` — 占位路由
9. 创建 `app.py` — 入口脚本
   ```python
   from app import create_app
   app = create_app()
   if __name__ == '__main__':
       app.run(debug=True)
   ```

**验收**: `python app.py` 启动无报错，`instance/blog.db` 自动生成。

### Milestone 2: 用户认证

**目标**: 实现注册、登录、退出功能，Flask-Login 管理会话。

**任务清单**:

1. 实现 `app/routes/auth.py` 注册路由
   - GET /register → 渲染注册表单
   - POST /register → 验证邮箱唯一性 + 密码 ≥6 字符
   - 使用 `generate_password_hash()` 哈希密码
   - 成功后 redirect 到 /login，flash 成功消息
2. 实现 `app/routes/auth.py` 登录路由
   - GET /login → 渲染登录表单
   - POST /login → `check_password_hash()` 验证
   - 成功后 `login_user()` → redirect 到 /
   - 失败时 flash 错误消息
3. 实现 `app/routes/auth.py` 退出路由
   - POST /logout → `logout_user()` → redirect 到 /
4. 配置 `login_manager.user_loader` 回调（在 extensions.py 或 models.py）
5. 创建 `templates/base.html` — 基础布局
   - 导航栏：首页 / 登录 / 注册 / 退出（按登录状态切换）
   - flash 消息显示区域
6. 创建 `templates/login.html` — 登录表单
7. 创建 `templates/register.html` — 注册表单

**验收**:
- 注册成功后数据库有新用户，密码为哈希值
- 登录后导航栏显示"退出"而非"登录"
- 退出后回到访客状态

### Milestone 3: 文章功能

**目标**: 实现文章创建、列表、详情、软删除。

**任务清单**:

1. 实现 `app/routes/posts.py` 首页路由
   - GET / → 查询 `Post.query.filter_by(is_deleted=0).order_by(Post.created_at.desc())`
   - 渲染文章列表
2. 实现 `app/routes/posts.py` 文章详情路由
   - GET /post/\<id\> → 查询文章（is_deleted=0），404 处理
   - 不显示作者信息
3. 实现 `app/routes/posts.py` 创建文章路由
   - GET /post/new → `@login_required`，渲染表单
   - POST /post/new → 验证 title/body 非空 → 保存
   - 成功后 redirect 到 /
4. 实现 `app/routes/posts.py` 删除文章路由
   - POST /post/\<id\>/delete → `@login_required` + 验证作者身份
   - 设置 `is_deleted = 1`，`db.session.commit()`
   - 非作者尝试删除 → 403 拒绝
5. 创建 `templates/index.html` — 文章列表
   - 标题可点击跳转详情页
   - 登录用户显示"New Post"按钮
6. 创建 `templates/post_detail.html` — 文章详情
   - 仅作者可见"Delete"按钮
7. 创建 `templates/post_new.html` — 发表文章表单

**验收**:
- 首页展示所有未删除文章，按时间倒序
- 登录后可发表文章，立即出现在首页
- 只有作者可见删除按钮，删除后文章消失
- 未登录访问 /post/new 被重定向到 /login

### Milestone 4: 错误处理 + 集成验证

**目标**: 完善全局错误处理，端到端验证全部功能。

**任务清单**:

1. 在 `app/__init__.py` 注册全局错误处理器
   - 404: 返回友好提示页面
   - 500: 返回友好提示页面
2. 在 `app/routes/posts.py` 添加 try/except
   - 数据库操作包裹异常处理
   - OperationalError / IntegrityError 处理
3. 确保 debug 模式下不暴露堆栈给用户（Flask 默认行为确认）
4. 完善所有 flash 消息文案（中文）
5. 端到端验证完整流程：
   - 访客 → 浏览首页/详情 → 无法创建/删除
   - 注册 → 登录 → 发表 → 看到文章 → 删除 → 文章消失
   - 未登录直接访问 /post/new → 跳转 /login
   - 注册重复邮箱 → 报错
   - 密码不足 6 位 → 报错
   - 空 title/body → 报错
   - 删除他人文章 → 403

**验收**: 全部 6 个用户场景通过，5 条成功标准满足。

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| 循环导入（models ↔ extensions） | Med | 扩展在 extensions.py 实例化，models 中 import 使用 |
| 单文件过大超过 200 行 | Med | 路由已按 auth/posts 拆分；models.py 仅两张表 |
| Flask-Login 与 SQLAlchemy 版本兼容 | Low | requirements.txt 锁定版本 |
| SECRET_KEY 硬编码风险 | Low | 优先读环境变量，仅开发环境用默认值 |

## Open Questions

- 无。规格已通过澄清，所有决策已落定。
