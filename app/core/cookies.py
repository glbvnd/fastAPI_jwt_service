from __future__ import annotations
from dataclasses import dataclass
from fastapi import Response, Cookie
from datetime import timedelta
from jose import jwt
from .config import settings


@dataclass(frozen=True)
class CookieSettings:
    access_name: str = "access_token"
    refresh_name: str = "refresh_token"
    secure: bool = False  # True in productions(HTTPS)
    samesite: str = "lax"  # lax |strict |none
    domain: str | None = None  # e.g. ".example.com"
    path: str = "/"
    access_ttl: timedelta = timedelta(minutes=15)
    refresh_ttl: timedelta = timedelta(days=7)


def set_cookies(
    response: Response,
    *,
    access_token: str,
    refresh_token: str,
    settings: CookieSettings = CookieSettings(),
) -> None:
    response.set_cookie(
        key=settings.access_name,
        value=access_token,
        max_age=int(settings.access_ttl.total_seconds()),
        httponly=True,
        secure=settings.secure,
        samesite=settings.samesite,
        path=settings.path,
        domain=settings.domain,
    )

    response.set_cookie(
        key=settings.refresh_name,
        value=refresh_token,
        max_age=int(settings.refresh_ttl.total_seconds()),
        httponly=True,
        secure=settings.secure,
        samesite=settings.samesite,
        path=settings.path,
        domain=settings.domain,
    )


def clear_cookies(
    response: Response, *, settings: CookieSettings = CookieSettings()
) -> None:
    response.delete_cookie(
        key=settings.access_name,
        path=settings.path,
        domain=settings.domain,
        httponly=True,
    )
    response.delete_cookie(
        key=settings.refresh_name,
        path=settings.path,
        domain=settings.domain,
        httponly=True,
    )
