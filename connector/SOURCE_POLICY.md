# Source Policy

Provider: Instagram

Policy snapshot: 2026-09-04. Reverify all live conditions before adapter work.

## Planned official surfaces

- read: professional_account_media
- read: comments
- read: mentions
- read: hashtag_media
- publication-plan target: image
- publication-plan target: video
- publication-plan target: reel
- publication-plan target: carousel
- publication-plan target: story
- deferred: consumer_account_access
- deferred: arbitrary_public_search

## Admission rules

- Official provider APIs and authorized accounts only.
- Every observation records source identity, time, URL, and permission basis.
- Account allowlists and topic allowlists are explicit configuration.
- Rate, quota, cost, retention, deletion, and review obligations fail closed.
- HTML scraping, session-cookie automation, CAPTCHA bypass, and stealth collection are out of scope.
- API success does not establish public visibility or consumer acceptance.

## Current provider boundary

Official API access is centered on authorized professional accounts. Consumer-account access and unrestricted public search are not assumed; Stories and other publishing surfaces must be rechecked against account type and current Meta review requirements.

Official documentation: https://developers.facebook.com/docs/instagram-platform/
