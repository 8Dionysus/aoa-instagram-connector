from __future__ import annotations

from aoa_instagram_connector.evidence import evidence_page


def test_evidence_page_preserves_provenance() -> None:
    page = evidence_page(
        {"user_id": "12345", "username": "owned_account"},
        {
            "data": [
                {
                    "id": "m1",
                    "media_type": "IMAGE",
                    "permalink": "https://www.instagram.com/p/example/",
                }
            ],
            "after": "cursor-1",
        },
        observed_at="2026-09-04T12:00:00Z",
    )

    assert page["network_effect"] == "read_only"
    assert page["next_after"] == "cursor-1"
    packet = page["items"][0]
    assert packet["schema"] == "aoa_social_evidence_packet_v1"
    assert packet["permission_basis"] == "instagram_business_basic"
    assert packet["source_url"] == "https://www.instagram.com/p/example/"
