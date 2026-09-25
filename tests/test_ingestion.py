from research_objects import ingest_lexisnexis, is_advanced_ai_usage_approved


def article(title: str, approval):
    return {"id": title, "title": title, "content": "text", "approvedForAdvancedAiUsage": approval}


def test_advanced_ai_approval_accepts_supported_true_values():
    assert is_advanced_ai_usage_approved(article("approved", "true"))
    assert is_advanced_ai_usage_approved(article("approved", True))
    assert is_advanced_ai_usage_approved(article("approved", " YES "))


def test_ingestion_filters_non_approved_articles_by_default():
    payload = {
        "articles": [
            article("approved", "true"),
            article("rejected", "false"),
            article("missing", None),
            article("unrecognized", "unknown"),
        ]
    }

    result = ingest_lexisnexis(payload)

    assert [item.title for item in result] == ["approved"]


def test_ingestion_can_include_articles_for_non_ai_audits():
    payload = {"articles": [article("approved", "true"), article("rejected", "false")]}

    result = ingest_lexisnexis(payload, approved_only=False)

    assert [item.title for item in result] == ["approved", "rejected"]
