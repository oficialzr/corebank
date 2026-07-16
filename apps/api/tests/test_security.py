from datetime import UTC, datetime, timedelta

import pytest
from corebank_api.core import security
from corebank_api.core.security import InvalidTokenError, create_access_token, decode_access_token


def test_create_and_decode_access_token_round_trip() -> None:
    token = create_access_token("alex@example.com")

    assert decode_access_token(token) == "alex@example.com"


def test_decode_access_token_rejects_expired_token(monkeypatch) -> None:
    fixed_now = datetime(2026, 7, 13, 12, 0, tzinfo=UTC)

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now if tz is not None else fixed_now.replace(tzinfo=None)

    monkeypatch.setattr(security, "datetime", FrozenDateTime)
    token = create_access_token("alex@example.com")
    monkeypatch.setattr(
        security,
        "datetime",
        type(
            "AdvancedDateTime",
            (datetime,),
            {
                "now": classmethod(
                    lambda cls, tz=None: (
                        fixed_now + timedelta(minutes=31)
                        if tz is not None
                        else (fixed_now + timedelta(minutes=31)).replace(tzinfo=None)
                    )
                )
            },
        ),
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)
