# Instagram Connector Charter

## Mission

Turn authorized Instagram surfaces into reproducible AoA evidence and
approval-ready publication plans while keeping external write effects explicit.

## Current phase

- preserve the independent repository owner and common social-connector contract
- provide Instagram Login configuration without storing secrets in Git
- perform bounded `/me` and owned-media reads
- normalize owned media into evidence packets
- keep publication, comments, messages, webhooks, and runtime effects disabled

## Success after source preparation

A later adapter may be called operational only after official API access, scoped
credentials, provider review, runtime admission, and ordinary consumer acceptance
are evidenced separately.

## Non-goals

- one universal implementation hiding provider differences
- secret storage inside the repository
- broad scraping or policy circumvention
- autonomous publication without an explicit approval contract
