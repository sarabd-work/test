from research_objects import ingest_statista


def test_statista_ingestion_supports_items_and_results():
    items = ingest_statista({"items": [{"identifier": "one", "title": "A"}]})
    results = ingest_statista({"results": [{"question_id": "two", "indicator": "B"}]})

    assert items[0].identifier == "one"
    assert items[0].title == "A"
    assert results[0].identifier == "two"
    assert results[0].title == "B"


def test_statista_ingestion_includes_all_records_by_default():
    payload = {
        "items": [
            {"title": "Premium", "is_premium": True},
            {"title": "Free", "is_premium": False},
            {"title": "Unmarked"},
        ]
    }

    assert [item.title for item in ingest_statista(payload)] == [
        "Premium",
        "Free",
        "Unmarked",
    ]


def test_statista_ingestion_can_filter_to_premium_records():
    payload = {
        "items": [
            {"title": "Premium", "is_premium": True},
            {"title": "Premium string", "is_premium": "true"},
            {"title": "Free", "is_premium": False},
        ]
    }

    assert [item.title for item in ingest_statista(payload, premium_only=True)] == [
        "Premium",
        "Premium string",
    ]
