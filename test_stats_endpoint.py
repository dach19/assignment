import requests
from constants import ENDPOINT_HASH, ENDPOINT_STATS, REQUEST_TIMEOUT


def test_app_returns_stats(start_stop_server):
    """
    Test app returns empty stats after startup
    HTTP Method: GET
    Endpoint: /stats
    """
    config = start_stop_server
    base_url = config['base_url']
    port = config['port']
    endpoint = f"{base_url}:{port}/{ENDPOINT_STATS}"
    r = requests.get(endpoint)
    stats = r.json()

    assert(r.status_code == 200)
    assert(stats["TotalRequests"] == 0)
    assert(stats["AverageTime"] == 0)

def test_app_stats_increases_after_requests(start_stop_server):
    """
    Test app stats requests count increases
    HTTP Method: POST
    Endpoint: /stats
    """
    config = start_stop_server
    base_url = config['base_url']
    port = config['port']

    endpoint_stats = f"{base_url}:{port}/{ENDPOINT_STATS}"
    endpoint_hash = f"{base_url}:{port}/{ENDPOINT_HASH}"
    REQUESTS = 3
    payload = { "password": "angrymonkey"}
    
    for i in range(REQUESTS):
        requests.post(endpoint_hash, json=payload, timeout=REQUEST_TIMEOUT)    
   
    r = requests.get(endpoint_stats)
    stats = r.json()

    assert(r.status_code == 200)
    assert(stats["TotalRequests"] == REQUESTS)
    assert(stats["AverageTime"] > 0)

