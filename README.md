# research-objects

A small, dependency-free Python library for turning Statista and LexisNexis/Moreover JSON responses into typed domain objects.

## Usage

```python
import requests
from research_objects import parse_lexisnexis, parse_statista

articles = parse_lexisnexis(requests.get(lexisnexis_url).json())
statistics = parse_statista(requests.get(statista_url, headers=headers).json())

print(articles[0].title)
print(statistics[0].covered_start)
```

`parse_lexisnexis` accepts both the collection response (`{"articles": [...]}`) and a single article object. `parse_statista` accepts the `items` responses used by the statistics and market-insights endpoints, the `results` response used by consumer insights, and a single result object.

The original API payload is retained on every object as `.raw`, while common fields are normalized into `Article` and `Statistic` dataclasses. The library does not make HTTP requests and therefore does not require API credentials.

## Development

```bash
python -m pip install -e .
python -m pytest
```
