from __future__ import annotations

import json

import aoa_instagram_connector.client as client_module
from aoa_instagram_connector.client import InstagramClient
from aoa_instagram_connector.config import Credentials


class FakeResponse:
    status = 200

    def __init__(self, payload: dict[str, object]) -> None:
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def read(self, _limit: int) -> bytes:
        return self.body


def credentials() -> Credentials:
    return Credentials(
        api_version="v26.0",
        access_token="IG" + ("x" * 48),
        source_path=None,
    )


def test_account_read_uses_bearer_header_not_query(monkeypatch) -> None:
    calls = []

    def fake_urlopen(request, *, timeout):
        calls.append((request, timeout))
        return FakeResponse(
            {
                "data": [
                    {
                        "user_id": "12345",
                        "username": "owned_account",
                        "account_type": "BUSINESS",
                        "media_count": 7,
                    }
                ]
            }
        )

    monkeypatch.setattr(client_module, "urlopen", fake_urlopen)
    account = InstagramClient(credentials()).get_account()

    assert account["user_id"] == "12345"
    assert account["username"] == "owned_account"
    request, timeout = calls[0]
    assert "access_token" not in request.full_url
    assert request.get_header("Authorization").startswith("Bearer IG")
    assert timeout == 20.0


def test_media_read_is_bounded_and_drops_unknown_fields(monkeypatch) -> None:
    def fake_urlopen(request, *, timeout):
        assert "limit=10" in request.full_url
        return FakeResponse(
            {
                "data": [
                    {
                        "id": "m1",
                        "media_type": "IMAGE",
                        "permalink": "https://www.instagram.com/p/example/",
                        "timestamp": "2026-09-01T10:00:00+0000",
                        "unexpected": "drop-me",
                    }
                ],
                "paging": {"cursors": {"after": "cursor-1"}},
            }
        )

    monkeypatch.setattr(client_module, "urlopen", fake_urlopen)
    page = InstagramClient(credentials()).list_media("12345", limit=10)

    assert page["after"] == "cursor-1"
    assert page["data"][0]["id"] == "m1"
    assert "unexpected" not in page["data"][0]
