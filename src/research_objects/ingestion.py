from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .models import Article
from .parsers import _payloads


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
    """Ingest LexisNexis articles, excluding non-approved articles by default.

    The filter is applied to raw records before they are converted into domain
    objects. Set ``approved_only=False`` only for auditing or non-AI workflows.
    Articles with a missing or unrecognized approval field are excluded when
    ``approved_only`` is enabled.
    """
    records = _payloads(payload, "articles")
    if approved_only:
        records = [record for record in records if is_advanced_ai_usage_approved(record)]
    return [Article.from_dict(record) for record in records]
