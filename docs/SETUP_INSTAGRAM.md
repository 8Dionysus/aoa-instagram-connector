# Connect an Instagram account

This is the fast owner-account path for Instagram API with Instagram Login.

## What Meta requires

- An Instagram professional account: Business or Creator.
- A Meta Business app with the Instagram product.
- The Instagram account added to the app while using Standard Access.
- A user access token with at least `instagram_business_basic`.

Instagram Login does not require a Facebook Page. Advanced Access and App Review
are required only when the app serves professional accounts you do not own or manage.

## Fast bootstrap

1. In the Meta App Dashboard, create or open a Business app.
2. Add **Instagram**, then open **API setup with Instagram login**.
3. Add the owner Instagram account and complete any tester invitation.
4. Click **Generate token**, sign in to Instagram, and grant
   `instagram_business_basic`.
5. On the connector host, create the owner-local file:

   ```bash
   PYTHONPATH=src python -m aoa_instagram_connector setup --json
   ```

6. Edit `~/.config/aoa-instagram-connector/credentials.env` locally and paste
   the token after `AOA_INSTAGRAM_ACCESS_TOKEN=`. Never paste it into chat.
7. Validate locally, then perform the bounded reads:

   ```bash
   PYTHONPATH=src python -m aoa_instagram_connector config-check --json
   PYTHONPATH=src python -m aoa_instagram_connector auth-check --json
   PYTHONPATH=src python -m aoa_instagram_connector media-list --limit 10 --json
   ```

The App Dashboard token is long-lived for approximately 60 days according to the
current Meta guide. Rotation/refresh must be admitted before unattended runtime use.

## Safety posture

- The access token is sent in the Authorization header, not in the URL.
- The credential file must be a regular, current-user-owned, non-symlink file
  with mode `0600`.
- Responses are size-bounded and output never includes the token.
- These commands perform reads only. Publication remains disabled.
- API version `v26.0` follows the current Meta Get Started example and is
  configurable because Meta documentation and app versions can differ.

Official sources:

- https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login
- https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/get-started
- https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/business-login
