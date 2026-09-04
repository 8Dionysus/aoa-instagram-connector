# aoa-instagram-connector

Policy-gated Instagram evidence and publication-plan connector for AoA.

Phase 1 source is prepared for Instagram API with Instagram Login. It can perform
two bounded reads against an authorized Business or Creator account: account
identity and one page of owned media. It contains no credentials and cannot
publish content.

## Owned here

- Instagram-specific source policy and capability discovery
- normalized evidence-packet and publication-plan contracts
- provider-specific parsing, preparation, validation, and local decisions
- a fail-closed local CLI, secret-file boundary, and repository validator

## Owned elsewhere

- cross-network campaign orchestration and editorial policy
- live MCP/HTTP composition, scheduling, queues, retries, and secret injection
- final publication authority and operator approval
- heavy captures, media, indexes, and generated corpora

## Current boundary

The admitted path is Instagram Login with `instagram_business_basic`. It does
not require a linked Facebook Page. Consumer accounts, arbitrary public search,
hashtag discovery, ads/tagging, comments, insights, webhooks, and every write
operation remain outside the first admission.

Official documentation:
https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login

API terms, scopes, quotas, review requirements, and pricing can change. Recheck
the official documentation before admitting a live account or runtime.

## Quick connection

```bash
python -m pip install -e ".[dev]"
aoa-instagram setup --json
# Fill ~/.config/aoa-instagram-connector/credentials.env locally.
aoa-instagram config-check --json
aoa-instagram auth-check --json
aoa-instagram media-list --limit 10 --json
```

The operator must generate the token in the Meta App Dashboard. Never paste a
token into chat. See [docs/SETUP_INSTAGRAM.md](docs/SETUP_INSTAGRAM.md).

## Bootstrap checks

```bash
python -m pip install -e ".[dev]"
python scripts/validate_connector.py
ruff check .
pytest
aoa-instagram doctor --json
```

A green bootstrap proves only source readiness. A successful `auth-check`
proves only the authorized account read, not runtime deployment, publication,
or consumer acceptance.
