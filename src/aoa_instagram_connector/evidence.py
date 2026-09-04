"""Normalize authorized Instagram media into AoA evidence packets."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

from aoa_instagram_connector import CONNECTOR_ID, PROVIDER


def evidence_page(
    account: dict[str, Any],
    media_page: dict[str, Any],
    *,
    observed_at: str | None = None,
) -> dict[str, Any]:
    timestamp = observed_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    username = str(account.get("username") or "")
    fallback_url = (
        f"https://www.instagram.com/{quote(username, safe='')}/"
        if username
        else "https://www.instagram.com/"
    )

    packets: list[dict[str, Any]] = []
    for media in media_page.get("data", []):
        if not isinstance(media, dict) or not media.get("id"):
            continue
        source_url = str(media.get("permalink") or fallback_url)
        packets.append(
            {
                "schema": "aoa_social_evidence_packet_v1",
                "provider": PROVIDER,
                "source_id": str(media["id"]),
                "source_url": source_url,
                "observed_at": timestamp,
                "permission_basis": "instagram_business_basic",
                "payload": dict(media),
            }
        )

    return {
        "schema": "aoa_social_evidence_page_v1",
        "connector_id": CONNECTOR_ID,
        "provider": PROVIDER,
        "observed_at": timestamp,
        "account": dict(account),
        "items": packets,
        "next_after": media_page.get("after"),
        "network_effect": "read_only",
    }
