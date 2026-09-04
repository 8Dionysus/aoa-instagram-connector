# aoa-instagram-connector Agent Guide

## Owner

This repository owns the portable Instagram connector source surface.
It is independently publishable and must remain usable without sibling repos.

The current admitted implementation is Instagram API with Instagram Login,
`instagram_business_basic`, `GET /me`, and one bounded owned-media page.

## Hard boundaries

- Use official, authorized provider APIs. Do not introduce scraping or bypasses by default.
- Keep credentials, tokens, account identifiers, raw exports, and media out of Git.
- Evidence reads and publication effects are separate planes.
- Publication stays disabled until an approval-gated effect owner is explicitly added.
- Runtime MCP/HTTP composition, queues, scheduling, retries, and secret injection belong to abyss-stack.
- Cross-platform campaign logic belongs to a future social orchestrator, not this connector.
- Treat provider policy, scopes, quotas, pricing, and review status as live facts to reverify.
- Read access tokens only from the owner-local mode-0600 file or process environment.
- Never place access tokens in URLs, logs, error messages, fixtures, or reports.

## Provider boundary

Instagram Login is limited to professional Business or Creator accounts and
does not require a linked Facebook Page. Standard Access is only for owned,
managed, or app-role accounts. Do not infer Advanced Access, hashtag search,
ads/tagging access, or publication permission from a successful basic read.

## Required checks

```bash
python -m pip install -e ".[dev]"
python scripts/validate_connector.py
ruff check .
pytest
aoa-instagram doctor --json
```

Do not claim live capability from these checks alone.
