# research-objects

A small, dependency-free Python library for turning Statista and LexisNexis/Moreover JSON responses into typed domain objects.

## Ingestion

Use `ingest_lexisnexis` for AI workflows. It filters the raw response before creating objects and **fails closed**: only records whose `approvedForAdvancedAiUsage` value is explicitly true are returned.

```python
from research_objects import ingest_lexisnexis, ingest_statista

articles = ingest_lexisnexis(lexisnexis_response)
statistics = ingest_statista(statista_response)
```

`ingest_statista` supports the `items` responses used by the statistics and market-insights endpoints, the `results` response used by consumer insights, and a single result object. All Statista records are included by default. To retain only records explicitly marked as premium, use:

```python
premium_statistics = ingest_statista(statista_response, premium_only=True)
```

To include non-approved LexisNexis records for an audit or non-AI workflow, opt out explicitly:

```python
audit_articles = ingest_lexisnexis(lexisnexis_response, approved_only=False)
```

The lower-level `parse_lexisnexis` and `parse_statista` functions remain available when no ingestion policy is needed. The original API payload is retained on every object as `.raw`.

## Development

```bash
python -m pip install -e .
python -m pytest
```
