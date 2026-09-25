import json
from pathlib import Path

from research_objects import Article, Statistic, parse_lexisnexis, parse_statista


ROOT = Path(__file__).parent


def test_lexisnexis_article_from_fixture():
    payload = json.loads((ROOT / "lexisnexis_output.txt").read_text())
    articles = parse_lexisnexis(payload)
    assert len(articles) == 1
    assert isinstance(articles[0], Article)
    assert articles[0].title.startswith("Gamma suitor")
    assert articles[0].companies[0].name == "BT Group PLC"
    assert articles[0].published_at is not None


def test_statista_statistics_and_insights():
    statistics = parse_statista(json.loads((ROOT / "statista3_output.txt").read_text()))
    insights = parse_statista(json.loads((ROOT / "statista2_output.txt").read_text()))
    assert isinstance(statistics[0], Statistic)
    assert statistics[0].identifier == 268416
    assert insights[0].title.startswith("Market share")
    assert insights[0].covered_start is not None
