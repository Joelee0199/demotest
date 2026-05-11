# Spec: Minimal Blog

> Created: 2026-05-08 | Status: DRAFT | Constitution Version: 1.0.0

## Summary

A minimalist personal blog system that allows users to register accounts,
log in, publish articles, and browse content. Unauthenticated visitors can
read all articles but cannot create or delete them. Only the article author
may delete their own posts. The system prioritizes simplicity: local-only
execution, no deployment pipeline, and a plain but functional UI.

## Constitutional Principles

- **P1 代码简洁清晰**: The spec demands only essential features —
  registration, login, article CRUD, and browsing — with no
  unnecessary complexity. Each user-facing function maps to one clear
  responsibility.
- **P2 Python 3.11+ & Flask**: The blog will be built with Flask,
  leveraging its lightweight routing and templating to stay minimal.
- **P3 SQLite 单一数据存储**: All user accounts and articles are
  stored in a single SQLite database file, requiring no external
  database service.
- **P4 密码哈希存储**: User passwords are never stored in plaintext;
  they are hashed before persistence and verified via constant-time
  comparison.
- **P5 接口错误处理**: Every route handles invalid input, missing
  resources, and unauthorized access with appropriate error responses
  and user-facing messages.
- **P6 文件行数限制**: The feature set is intentionally small so that
  each source file stays well under 200 lines; routes are split by
  domain (auth vs. posts).

> If any principle is violated, the spec MUST be rejected or the
> constitution MUST be formally amended first.

## User Scenarios & Testing

### Scenario 1: New User Registration

A visitor arrives at the blog, clicks "Register", enters an email and
password, and becomes a registered user. After successful registration,
they are redirected to the login page.

**Acceptance**: A new account appears in the database; the password
is stored as a hash, not plaintext.

### Scenario 2: User Login and Logout

A registered user enters their email and password on the login page.
Upon successful authentication, they are redirected to the homepage with
a visible indicator that they are logged in. Clicking "Logout" ends
the session and returns them to the homepage as a visitor.

**Acceptance**: Logged-in state is maintained across page navigations;
logging out clears the session.

### Scenario 3: Browsing Articles (Unauthenticated)

A visitor opens the homepage and sees a list of articles sorted by
creation time (newest first). Clicking an article title opens the
detail page showing the full content (no author information is
displayed). The visitor cannot create or delete articles.

**Acceptance**: Article list displays all published articles; detail
page shows title and body only; "New Post" and "Delete" controls are
not visible to unauthenticated users.

### Scenario 4: Publishing an Article

A logged-in user clicks "New Post", fills in a title and body, and
submits. The article appears immediately on the homepage.

**Acceptance**: The new article appears in the list; the author is
recorded correctly.

### Scenario 5: Deleting an Article

A logged-in user views an article they authored and clicks "Delete".
The article is soft-deleted — it is marked as deleted and no longer
appears on the homepage, but its data is retained in the database.
Another user (or visitor) cannot see the delete button on articles
they did not author.

**Acceptance**: Deleted articles are no longer visible on the site;
the database record is retained with a deletion marker; only the
author sees the delete control.

### Scenario 6: Unauthorized Actions

A visitor attempts to access the "New Post" page directly via URL.
They are redirected to the login page. A logged-in user attempts to
delete another user's article; the request is rejected.

**Acceptance**: Protected pages require authentication; cross-author
deletion is blocked.

## Requirements

### Functional Requirements

| ID    | Requirement                                                          | Priority |
|-------|----------------------------------------------------------------------|----------|
| FR-001| Users can register with email and password (minimum 6 characters)    | Must     |
| FR-002| Users can log in with email and password                             | Must     |
| FR-003| Users can log out                                                    | Must     |
| FR-004| Unauthenticated users can browse the article list on the homepage    | Must     |
| FR-005| Unauthenticated users can view article detail pages                  | Must     |
| FR-006| Authenticated users can create articles with title and body           | Must     |
| FR-007| Articles on the homepage are listed in reverse chronological order  | Must     |
| FR-008| Only the article author can delete their own articles                | Must     |
| FR-009| Deleted articles are soft-deleted (marked as deleted, data retained)| Must     |
| FR-010| Unauthenticated users are redirected to login when accessing        | Must     |
|       | protected pages                                                      |          |
| FR-011| Duplicate email registration is rejected with a clear message        | Must     |
| FR-012| Invalid login credentials are rejected with a clear message         | Must     |
| FR-013| Passwords shorter than 6 characters are rejected at registration    | Must     |
| FR-014| Article title and body are required fields; empty submission is      | Must     |
|       | rejected                                                             |          |

### Non-Functional Requirements

| ID     | Requirement                                                  | Principle |
|--------|--------------------------------------------------------------|-----------|
| NFR-001| Passwords MUST be stored as hashes, never plaintext          | P4        |
| NFR-002| All pages MUST render within 2 seconds on localhost        | P1, P3    |
| NFR-003| Every route MUST handle errors gracefully without stack      | P5        |
|        | traces exposed to users                                      |           |
| NFR-004| Each source file MUST NOT exceed 200 lines                  | P6        |
| NFR-005| The application MUST run locally with no external            | P2, P3    |
|        | database or service dependencies                             |           |

## API Design

### Endpoints

| Method | Path         | Description                  | Auth  |
|--------|--------------|------------------------------|-------|
| GET    | /            | Homepage — article list      | No    |
| GET    | /login       | Login page                   | No    |
| POST   | /login       | Submit login credentials     | No    |
| GET    | /register    | Registration page            | No    |
| POST   | /register    | Submit registration data     | No    |
| POST   | /logout      | End session                  | Yes   |
| GET    | /post/new    | New article form             | Yes   |
| POST   | /post/new    | Submit new article           | Yes   |
| GET    | /post/\<id\> | Article detail page           | No    |
| POST   | /post/\<id\>/delete | Soft-delete article            | Yes (author only) |

### Error Responses

All endpoints MUST return errors in the following format (P5):

```json
{
  "error": "NOT_FOUND",
  "message": "Human-readable description"
}
```

For page routes, errors display a user-friendly message page rather
than JSON. For form submissions, errors are shown as flash messages
on the originating form page.

## Data Model

All data MUST be stored in SQLite (P3).

| Table  | Fields                                                        | Constraints                                        |
|--------|---------------------------------------------------------------|----------------------------------------------------|
| user   | id (INTEGER PK), email (TEXT), password_hash (TEXT),         | email UNIQUE, NOT NULL; password_hash NOT NULL      |
|        | created_at (TEXT)                                             | created_at NOT NULL, default current timestamp      |
| post   | id (INTEGER PK), title (TEXT), body (TEXT), author_id (INT), | title NOT NULL; body NOT NULL; author_id FK→user.id|
|        | is_deleted (INTEGER), created_at (TEXT)                       | is_deleted NOT NULL, default 0; created_at NOT NULL |

## File Structure

Each file MUST NOT exceed 200 lines (P6).

```
app/
├── __init__.py          # Flask app factory
├── config.py            # Configuration
├── models.py            # SQLAlchemy models (User, Post)
├── routes/
│   ├── auth.py          # Login, register, logout routes
│   └── posts.py         # Article list, detail, create, delete routes
├── templates/
│   ├── base.html        # Shared layout
│   ├── index.html       # Homepage — article list
│   ├── login.html       # Login form
│   ├── register.html    # Registration form
│   ├── post_detail.html # Article detail page
│   └── post_new.html    # New article form
└── db.py                # Database initialization helper
run.py                   # Entry point: python run.py
requirements.txt         # Pinned dependencies
```

## Assumptions

- **Single-author focus**: Although multiple users can register, the
  blog is designed for personal use; no admin panel or role system is
  needed.
- **Soft delete**: Articles are soft-deleted (marked with `is_deleted=1`
  in the database) rather than permanently removed, allowing potential
  recovery while keeping the feature simple.
- **No article editing**: Only create and delete are supported; editing
  is out of scope for this version.
- **No pagination**: The homepage shows all articles; pagination is
  deferred until article count warrants it.
- **No rich text**: Article body is plain text; no Markdown or HTML
  rendering in this version.
- **Session-based auth**: Uses Flask's built-in session cookies with a
  secret key; no JWT or OAuth.
- **No email verification**: Registration is immediate; no confirmation
  email is sent.
- **No author display**: Article detail pages show only title and body;
  author information is not displayed to keep the UI minimal.

## Success Criteria

1. A new user can register, log in, and see the homepage with their
   logged-in status displayed — completing the flow in under 1 minute.
2. A logged-in user can publish an article and see it appear on the
   homepage immediately after submission.
3. Unauthenticated visitors can browse all articles and view details
   but cannot access protected actions (create/delete).
4. Only the article author can delete their own articles; deleted
   articles are soft-deleted (hidden from view but retained in the
   database); all other deletion attempts are rejected.
5. The application starts and is usable with a single command on a
   local machine with Python 3.11+ installed.
