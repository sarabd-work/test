from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .models import Article, Statistic


def _payloads(payload: Mapping[str, Any], key: str) -> list[Mapping[str, Any]]:
    """Return result records from a single-record or collection API response."""
    records = payload.get(key)
    if records is None:
        return [payload]
    if isinstance(records, Mapping):
        return [records]
    return [record for record in records if isinstance(record, Mapping)]


def parse_lexisnexis(payload: Mapping[str, Any]) -> list[Article]:
    """Parse a LexisNexis/Moreover response without applying licensing filters.

    For AI ingestion, prefer :func:`research_objects.ingest_lexisnexis`, which
    excludes records that are not approved for advanced AI usage.
    """
    return [Article.from_dict(item) for item in _payloads(payload, "articles")]


def parse_statista(payload: Mapping[str, Any]) -> list[Statistic]:
    """Parse Statista statistics, market insights, or consumer-insights responses."""
    records = payload.get("items")
    if records is None:
        records = payload.get("results")
    if records is None:
        records = [payload]
    if isinstance(records, Mapping):
        records = [records]
    return [Statistic.from_dict(item) for item in records if isinstance(item, Mapping)]
