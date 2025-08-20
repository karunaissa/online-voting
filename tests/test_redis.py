def test_redis_connection(client):
    r = client.application.redis
    r.set("test_key", "123")
    val = r.get("test_key")
    assert val == "123"
