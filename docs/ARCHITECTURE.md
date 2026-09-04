# Architecture

## Current source surface

```text
official Instagram API
             |
 read-only client (implemented, unadmitted)
             |
 policy gate -> normalized evidence packet
             |
       agent selection/preparation
             |
 publication plan (no external effect)
             |
 approval-gated publisher/runtime (external owner, disabled)
```

The repository owns provider-specific interpretation and portable contracts.
A future social orchestrator may coordinate multiple connectors through those
contracts, but it must not absorb provider credentials or policy decisions.

## Base components

- connector/manifest.json: declared capabilities and effect posture
- connector/schemas/: starter interoperability contracts
- connector/profiles/starter.json: secret-free offline profile
- src/: installable doctor CLI with no network path
- scripts/validate_connector.py: public-safety and identity checks

## Phase 1 additions

- config.py: strict mode-0600 credential loading with no token output
- client.py: size- and time-bounded Bearer-authenticated GET requests
- evidence.py: provider records normalized into AoA evidence packets
- CLI: setup, config-check, auth-check, and media-list

No MCP/HTTP runtime, token refresh service, webhook receiver, or publication
adapter is present.
