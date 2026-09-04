# Boundaries

## Plane split

| Plane | Phase 0 state | Effect |
| --- | --- | --- |
| Owned profile/media read | implemented, not live-admitted | read-only |
| Draft preparation | planned | no external effect |
| Publication plan | planned | no external effect |
| Publication commit | disabled | external write, approval required |

A publication plan is data, not permission. A successful API submission is not
the same claim as processing completion, public visibility, or consumer acceptance.

## Provider-specific admission

The current admission is Instagram Login, `instagram_business_basic`, and an
owned Business or Creator account. A successful basic read does not admit
comments, messages, insights, webhooks, hashtag search, ads/tagging, or writes.

## Data and privacy

- Collect only fields required by an admitted use case.
- Preserve source identity, observation time, URL, and permission basis.
- Apply current deletion, refresh, retention, and user-revocation duties.
- Store large or sensitive state outside Git under operator-owned paths.
