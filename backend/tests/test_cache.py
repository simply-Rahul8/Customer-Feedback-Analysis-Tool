from backend.cache import cache_result, get_cached_result

def test_cache_saves_and_returns(test_db):
    cache_result(test_db, "hello", "Positive", "greeting", "No")

    cached = get_cached_result(test_db, "hello")

    assert cached is not None
    assert cached.sentiment == "Positive"
    assert cached.topics == "greeting"
    assert cached.alert == "No"
