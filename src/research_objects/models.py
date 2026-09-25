from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping


def _datetime(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


@dataclass(frozen=True, slots=True)
class CompanyMention:
    """A company identified in a LexisNexis article."""

    name: str
    symbol: str | None = None
    exchange: str | None = None
    isin: str | None = None
    primary: bool = False
    title_count: int = 0
    content_count: int = 0

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "CompanyMention":
        return cls(
            name=str(value.get("name", "")),
            symbol=value.get("symbol"),
            exchange=value.get("exchange"),
            isin=value.get("isin"),
            primary=bool(value.get("primary", False)),
            title_count=int(value.get("titleCount", 0) or 0),
            content_count=int(value.get("contentCount", 0) or 0),
        )


@dataclass(frozen=True, slots=True)
class Article:
    """Normalized article returned by the LexisNexis/Moreover API."""

    title: str
    content: str
    source: str | None = None
    url: str | None = None
    article_id: str | None = None
    language: str | None = None
    language_code: str | None = None
    published_at: datetime | None = None
    harvested_at: datetime | None = None
    topics: tuple[str, ...] = ()
    companies: tuple[CompanyMention, ...] = ()
    sentiment_score: float | None = None
    raw: Mapping[str, Any] = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Article":
        sentiment = value.get("sentiment") or {}
        source = value.get("source") or {}
        topics = tuple(
            str(item.get("name", item)) if isinstance(item, Mapping) else str(item)
            for item in (value.get("topics") or [])
        )
        return cls(
            title=str(value.get("title", "")),
            content=str(value.get("content", "")),
            source=source.get("name") or value.get("sourceName"),
            url=value.get("url"),
            article_id=str(value["id"]) if value.get("id") is not None else None,
            language=value.get("language"),
            language_code=value.get("languageCode"),
            published_at=_datetime(value.get("publishedDate")),
            harvested_at=_datetime(value.get("harvestDate")),
            topics=topics,
            companies=tuple(CompanyMention.from_dict(item) for item in (value.get("companies") or [])),
            sentiment_score=float(sentiment["score"]) if sentiment.get("score") is not None else None,
            raw=value,
        )


@dataclass(frozen=True, slots=True)
class Statistic:
    """Normalized Statista result. Fields support both statistics and insights APIs."""

    title: str
    identifier: str | int | None = None
    subject: str | None = None
    description: str | None = None
    link: str | None = None
    is_premium: bool | None = None
    released_at: datetime | None = None
    updated_at: datetime | None = None
    covered_start: datetime | None = None
    covered_end: datetime | None = None
    geographies: tuple[str, ...] = ()
    industries: tuple[str, ...] = ()
    raw: Mapping[str, Any] = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Statistic":
        timeframe = value.get("covered_time_frame") or value.get("covered_timeframe") or {}
        geos = value.get("geolocations") or value.get("covered_geos") or []
        industries = value.get("industries") or []
        geography_names = tuple(
            (item.get("name") or item.get("code", "")) if isinstance(item, Mapping) else str(item)
            for item in (geos.values() if isinstance(geos, Mapping) else geos)
        )
        industry_names = tuple(
            item.get("name", "") if isinstance(item, Mapping) else str(item)
            for item in industries
        )
        return cls(
            title=str(value.get("title", value.get("indicator", ""))),
            identifier=value.get("identifier", value.get("question_id")),
            subject=value.get("subject"),
            description=value.get("description"),
            link=value.get("link"),
            is_premium=value.get("is_premium"),
            released_at=_datetime(value.get("released_at")),
            updated_at=_datetime(value.get("updated_at")),
            covered_start=_datetime(timeframe.get("start")),
            covered_end=_datetime(timeframe.get("end")),
            geographies=geography_names,
            industries=industry_names,
            raw=value,
        )
