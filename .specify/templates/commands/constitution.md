---
name: constitution
description: Update the project constitution with new or revised principles
allowed-tools:
  - read_file
  - write_to_file
  - replace_in_file
  - search_file
  - search_content
  - list_dir
---

# Constitution Update Command

## Instructions

1. Read the current constitution at `.specify/memory/constitution.md`.
2. Identify placeholder tokens or principles that need updating.
3. Collect values from user input or infer from project context.
4. Draft the updated constitution following semantic versioning:
   - MAJOR: principle removal or redefinition
   - MINOR: new principle or materially expanded guidance
   - PATCH: clarifications, wording fixes
5. Validate: no remaining bracket tokens, version matches report.
6. Write the updated constitution back to `.specify/memory/constitution.md`.
7. Check dependent templates for consistency and update if needed.
8. Output a summary with version, bump rationale, and commit message.
