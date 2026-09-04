# AOA-INSTAGRAM-D-0002 — Instagram Login basic-read bootstrap

- Status: Accepted
- Date: 2026-09-04
- Accepted by: Operator-authorized implementation

## Context

The operator authorized connecting the social providers one at a time, starting
with the preparation needed for the first provider. Meta currently exposes two
different Instagram API login contours. Facebook Login requires a connected
Facebook Page; Instagram Login can manage an owned Business or Creator account
without that Page dependency.

The first connection must be fast, secret-safe, and unable to publish.

## Decision

Use Instagram API with Instagram Login as the primary Phase 1 contour. Admit only
the `instagram_business_basic` read scope and the `/me` plus owned
`/<IG_ID>/media` requests.

Bootstrap with a long-lived token generated in the Meta App Dashboard and stored
in the owner-local mode-0600 credential file. Keep the full browser callback,
short-to-long token exchange, unattended refresh, comments, insights, webhooks,
and publication outside this admission.

## Alternatives considered

- Instagram API with Facebook Login and a required connected Facebook Page.
- A complete Business Login callback server and token lifecycle immediately.
- A manual App Dashboard token for the owned account, with the connector already
  shaped for the same Instagram Login API.

The third alternative is accepted for the first connection.

## Rationale

It minimizes setup and secret exposure while proving the real provider identity
and owned-media read path. It avoids storing an Instagram App Secret for the
initial probe and does not make a temporary bootstrap flow the runtime owner.

## Consequences

- The Instagram account must be Business or Creator.
- The operator must generate and rotate the token; current Meta guidance gives
  App Dashboard tokens a 60-day lifetime.
- Standard Access is sufficient only for accounts owned or managed by an app
  role; other accounts require Advanced Access and App Review.
- The API version remains configurable because Meta versions and documentation
  can move independently.
- Publication authority remains disabled.

## Owner and source surfaces

- src/aoa_instagram_connector/config.py
- src/aoa_instagram_connector/client.py
- src/aoa_instagram_connector/evidence.py
- docs/SETUP_INSTAGRAM.md
- connector/manifest.json
- connector/SOURCE_POLICY.md
- tests/

## Effect authority

The operator authorized source preparation and an owner-local empty credential
template. This decision does not authorize creation of a Meta app, generation or
entry of a token by the agent, publication, messages, comments, or runtime
deployment.

## Follow-up

After the operator fills the local token file, run one `auth-check` and one
bounded `media-list`. Treat them as API connectivity evidence only; runtime
admission and consumer acceptance remain separate.
