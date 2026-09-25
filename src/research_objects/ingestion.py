from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .models import Article, Statistic
from .parsers import _payloads, parse_statista


_TRUE_VALUES = {True, 1, "1", "true", "yes", "y", "on"}


def is_advanced_ai_usage_approved(article: Mapping[str, Any]) -> bool:
    """Return whether LexisNexis explicitly approves an article for advanced AI use.

    LexisNexis currently returns ``approvedForAdvancedAiUsage`` as a string, but
    this accepts booleans and common serialized boolean values as well. Missing,
    null, or unrecognized values are rejected intentionally (fail closed).
    """
    value = article.get("approvedForAdvancedAiUsage")
    if isinstance(value, str):
        value = value.strip().lower()
    return value in _TRUE_VALUES


def ingest_lexisnexis(
    payload: Mapping[str, Any], *, approved_only: bool = True
) -> list[Article]:
    """Ingest LexisNexis articles, excluding non-approved articles by default."""
    records = _payloads(payload, "articles")
    if approved_only:
        records = [record for record in records if is_advanced_ai_usage_approved(record)]
    return [Article.from_dict(record) for record in records]


def _is_premium(statistic: Statistic) -> bool:
    """Normalize Statista's optional premium flag for filtering."""
    value = statistic.is_premium
    if isinstance(value, str):
        value = value.strip().lower()
    return value in _TRUE_VALUES


def ingest_statista(
    payload: Mapping[str, Any], *, premium_only: bool = False
) -> list[Statistic]:
    """Ingest Statista API responses into :class:`Statistic` objects.

    Supports the ``items`` shape returned by the statistics and market-insights
    endpoints, the ``results`` shape returned by consumer insights, and a single
    result object. All records are included by default; pass ``premium_only``
    when a workflow should retain only records explicitly marked premium.
    """
    statistics = parse_statista(payload)
    if premium_only:
        statistics = [statistic for statistic in statistics if _is_premium(statistic)]
    return statistics
