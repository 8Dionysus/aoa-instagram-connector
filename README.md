# aoa-instagram-connector

Policy-gated Instagram evidence and publication-plan connector for AoA.

Phase 0 is an offline, policy-first skeleton. It makes no live API calls,
contains no credentials, and cannot publish content.

## Owned here

- Instagram-specific source policy and capability discovery
- normalized evidence-packet and publication-plan contracts
- provider-specific parsing, preparation, validation, and local decisions
- a fail-closed local CLI and repository validator

## Owned elsewhere

- cross-network campaign orchestration and editorial policy
- live MCP/HTTP composition, scheduling, queues, retries, and secret injection
- final publication authority and operator approval
- heavy captures, media, indexes, and generated corpora

## Current boundary

Official API access is centered on authorized professional accounts. Consumer-account access and unrestricted public search are not assumed; Stories and other publishing surfaces must be rechecked against account type and current Meta review requirements.

Official documentation: https://developers.facebook.com/docs/instagram-platform/

API terms, scopes, quotas, review requirements, and pricing can change. Recheck
the official documentation before implementing or admitting a live adapter.

## Bootstrap checks

```bash
python -m pip install -e ".[dev]"
python scripts/validate_connector.py
ruff check .
pytest
aoa-instagram doctor --json
```

A green bootstrap proves only the source skeleton. It does not prove API access,
OAuth, deployment, publication, or consumer acceptance.
