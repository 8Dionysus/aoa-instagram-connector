# Source Policy

Provider: Instagram

Policy snapshot: 2026-09-04. Reverify all live conditions before adapter work.

## Implemented, awaiting owner token

- read: professional_account_profile via `GET /me`
- read: one bounded page of professional_account_media

Required scope: `instagram_business_basic`.

## Planned official surfaces

- read: comments
- read: mentions
- read: media_insights
- publication-plan target: image
- publication-plan target: video
- publication-plan target: reel
- publication-plan target: carousel
- publication-plan target: story
- deferred: consumer_account_access
- deferred: arbitrary_public_search
- deferred: hashtag_media
- deferred: ads_and_tagging

## Admission rules

- Official provider APIs and authorized accounts only.
- Every observation records source identity, time, URL, and permission basis.
- Account allowlists and topic allowlists are explicit configuration.
- Rate, quota, cost, retention, deletion, and review obligations fail closed.
- HTML scraping, session-cookie automation, CAPTCHA bypass, and stealth collection are out of scope.
- API success does not establish public visibility or consumer acceptance.

## Current provider boundary

Instagram Login supports professional Business and Creator accounts without a
linked Facebook Page. It does not grant consumer-account, ads, or tagging
access. Standard Access applies only to accounts owned or managed by an app
role; broader service requires Advanced Access and App Review.

Official documentation:
https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login
