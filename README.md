# research-objects

A small, dependency-free Python library for turning Statista and LexisNexis/Moreover JSON responses into typed domain objects.

## LexisNexis AI-safe ingestion

Use `ingest_lexisnexis` for AI workflows. It filters the raw response before creating objects and **fails closed**: only records whose `approvedForAdvancedAiUsage` value is explicitly true are returned. The API's string values (`"true"`/`"false"`) and boolean values are supported.

```python
from research_objects import ingest_lexisnexis

articles = ingest_lexisnexis(lexisnexis_response)
```

To include non-approved records for an audit or non-AI workflow, opt out explicitly:

```python
articles = ingest_lexisnexis(lexisnexis_response, approved_only=False)
```

`parse_lexisnexis` remains available as an unfiltered parser. For AI ingestion, use `ingest_lexisnexis` so records without approval are not accidentally processed.

## Statista

```python
from research_objects import parse_statista

statistics = parse_statista(statista_response)
```

The parsers accept collection responses and single objects. The original API payload is retained on every object as `.raw`, while common fields are normalized into `Article` and `Statistic` dataclasses. The library does not make HTTP requests and therefore does not require API credentials.

## Development

```bash
python -m pip install -e .
python -m pytest
```
