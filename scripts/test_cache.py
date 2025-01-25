from datetime import datetime
from app.utils.cache import cache_events, get_cached_events

def test_cache_functionality():
    """
    Test the caching functionality for storing and retrieving events.
    """
    # Test key and data
    test_key = "test:events"
    test_data = [{"id": 1, "timestamp": datetime.now()}]

    # Cache the test data
    cache_events(test_key, test_data)

    # Retrieve the cached data
    cached_data = get_cached_events(test_key)

    # Print the result
    print("Cached Data:", cached_data)

if __name__ == "__main__":
    test_cache_functionality()
