"""Bounded read-only client for Instagram API with Instagram Login."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from aoa_instagram_connector import CONNECTOR_ID, __version__
from aoa_instagram_connector.config import Credentials

GRAPH_BASE_URL = "https://graph.instagram.com"
ACCOUNT_FIELDS = (
    "user_id",
    "username",
    "name",
    "account_type",
    "profile_picture_url",
    "followers_count",
    "follows_count",
    "media_count",
)
MEDIA_FIELDS = (
    "id",
    "media_type",
    "media_url",
    "permalink",
    "thumbnail_url",
    "timestamp",
    "username",
)


class InstagramError(RuntimeError):
    """Base class for safe connector failures."""


class InstagramTransportError(InstagramError):
    """The API could not be reached or returned malformed transport data."""


@dataclass(frozen=True)
class InstagramAPIError(InstagramError):
    status: int | None
    error_type: str | None
    code: int | None
    subcode: int | None
    safe_message: str

    def __str__(self) -> str:
        parts = [self.safe_message]
        if self.code is not None:
            parts.append(f"code={self.code}")
        if self.subcode is not None:
            parts.append(f"subcode={self.subcode}")
        if self.status is not None:
            parts.append(f"http={self.status}")
        return "; ".join(parts)


class InstagramClient:
    def __init__(
        self,
        credentials: Credentials,
        *,
        timeout_seconds: float = 20.0,
        max_response_bytes: int = 2_000_000,
    ) -> None:
        self.credentials = credentials
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes

    def get_account(self) -> dict[str, Any]:
        payload = self._get("me", {"fields": ",".join(ACCOUNT_FIELDS)})
        candidate: Any = payload
        if isinstance(payload.get("data"), list):
            data = payload["data"]
            candidate = data[0] if data else None
        elif isinstance(payload.get("data"), dict):
            candidate = payload["data"]

        if not isinstance(candidate, dict):
            raise InstagramTransportError("Instagram /me response did not contain an account")

        user_id = candidate.get("user_id") or candidate.get("id")
        if not user_id:
            raise InstagramTransportError("Instagram /me response did not contain user_id")

        result = {
            field: candidate[field]
            for field in ACCOUNT_FIELDS
            if field in candidate and candidate[field] is not None
        }
        result["user_id"] = str(user_id)
        return result

    def list_media(self, user_id: str, *, limit: int = 25) -> dict[str, Any]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")

        payload = self._get(
            f"{quote(str(user_id), safe='')}/media",
            {"fields": ",".join(MEDIA_FIELDS), "limit": str(limit)},
        )
        data = payload.get("data")
        if not isinstance(data, list):
            raise InstagramTransportError("Instagram media response did not contain a data list")

        items: list[dict[str, Any]] = []
        for candidate in data:
            if not isinstance(candidate, dict) or not candidate.get("id"):
                continue
            items.append(
                {
                    field: candidate[field]
                    for field in MEDIA_FIELDS
                    if field in candidate and candidate[field] is not None
                }
            )

        paging = payload.get("paging")
        after: str | None = None
        if isinstance(paging, dict):
            cursors = paging.get("cursors")
            if isinstance(cursors, dict) and cursors.get("after"):
                after = str(cursors["after"])

        return {"data": items, "after": after}

    def _get(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        version = quote(self.credentials.api_version, safe=".")
        url = f"{GRAPH_BASE_URL}/{version}/{path}?{urlencode(params)}"
        request = Request(
            url,
            headers={
                "Authorization": f"Bearer {self.credentials.access_token}",
                "Accept": "application/json",
                "User-Agent": f"{CONNECTOR_ID}/{__version__}",
            },
            method="GET",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                status = getattr(response, "status", 200)
                body = response.read(self.max_response_bytes + 1)
        except HTTPError as exc:
            body = exc.read(self.max_response_bytes + 1)
            payload = self._decode_json(body, allow_error=True)
            raise self._api_error(payload, status=exc.code) from None
        except (URLError, TimeoutError, OSError) as exc:
            raise InstagramTransportError(
                f"Instagram API transport failed: {type(exc).__name__}"
            ) from None

        if len(body) > self.max_response_bytes:
            raise InstagramTransportError("Instagram API response exceeded the size limit")

        payload = self._decode_json(body)
        if "error" in payload or "error_type" in payload:
            raise self._api_error(payload, status=status)
        return payload

    def _decode_json(self, body: bytes, *, allow_error: bool = False) -> dict[str, Any]:
        if len(body) > self.max_response_bytes:
            raise InstagramTransportError("Instagram API response exceeded the size limit")
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            if allow_error:
                return {}
            raise InstagramTransportError("Instagram API returned invalid JSON") from None
        if not isinstance(payload, dict):
            raise InstagramTransportError("Instagram API returned a non-object JSON response")
        return payload

    def _api_error(self, payload: dict[str, Any], *, status: int | None) -> InstagramAPIError:
        error = payload.get("error")
        if not isinstance(error, dict):
            error = payload
        raw_message = str(
            error.get("message")
            or error.get("error_message")
            or "Instagram API request failed"
        )
        safe_message = raw_message.replace(self.credentials.access_token, "[redacted]")
        code = error.get("code")
        subcode = error.get("error_subcode")
        return InstagramAPIError(
            status=status,
            error_type=str(error.get("type")) if error.get("type") else None,
            code=code if isinstance(code, int) else None,
            subcode=subcode if isinstance(subcode, int) else None,
            safe_message=safe_message,
        )
