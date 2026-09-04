# aoa-instagram-connector Agent Guide

## Owner

This repository owns the portable Instagram connector source surface.
It is independently publishable and must remain usable without sibling repos.

## Hard boundaries

- Use official, authorized provider APIs. Do not introduce scraping or bypasses by default.
- Keep credentials, tokens, account identifiers, raw exports, and media out of Git.
- Evidence reads and publication effects are separate planes.
- Publication stays disabled until an approval-gated effect owner is explicitly added.
- Runtime MCP/HTTP composition, queues, scheduling, retries, and secret injection belong to abyss-stack.
- Cross-platform campaign logic belongs to a future social orchestrator, not this connector.
- Treat provider policy, scopes, quotas, pricing, and review status as live facts to reverify.

## Provider boundary

Official API access is centered on authorized professional accounts. Consumer-account access and unrestricted public search are not assumed; Stories and other publishing surfaces must be rechecked against account type and current Meta review requirements.

## Required checks

```bash
python -m pip install -e ".[dev]"
python scripts/validate_connector.py
ruff check .
pytest
aoa-instagram doctor --json
```

Do not claim live capability from these checks alone.
