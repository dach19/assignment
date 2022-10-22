import requests
import concurrent.futures
import pytest
from start_stop_server import start_server, stop_server
from constants import ENDPOINT_HASH, ENDPOINT_STATS, REQUEST_TIMEOUT


def get_status(endpoint, payload):
    r = requests.post(endpoint, json=payload, timeout=REQUEST_TIMEOUT)
    return r.status_code

def get_status_error(endpoint, payload):
    with pytest.raises(Exception) as e_info:
        requests.post(endpoint, json=payload, timeout=REQUEST_TIMEOUT)
    return e_info.value

def test_app_accepts_multiple_requests(start_stop_server):
    """
    Test app can handle multiple requests simultaneously,
    Get stats to validate all requests were successful
    HTTP Method: POST
    Endpoint: /hash
    """
    config = start_stop_server
    base_url = config['base_url']
    port = config['port']
    # start_server(port)
    endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}"
    stats_endpoint = f"{base_url}:{port}/{ENDPOINT_STATS}"
    
    REQUESTS = 10

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for number in range(REQUESTS):
            payload1 = { "password": f"angrymonkey{number + 100}"}
            payload2 = { "password": f"ravingRabbids{number * 10}"}
            futures.append(executor.submit(get_status, endpoint=endpoint, payload=payload1))
            futures.append(executor.submit(get_status, endpoint=endpoint, payload=payload2))

    for future in concurrent.futures.as_completed(futures):
        assert(future.result() == 200)
    r = requests.post(stats_endpoint)
    stats = r.json()
    assert(stats["TotalRequests"] == (REQUESTS  * 2))
    

def test_app_shutdowns_gracefully(config):
    """
    Test app should complete any inflight request after shutdown
    Should also reject new requests
    HTTP Method: POST
    Endpoint: /hash
    """
    REQUESTS = 5
    base_url = config['base_url']
    port = config['port']
    start_server(port)

    endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}"
    accepted_requests = []
    not_accepted_requests = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for request in range(REQUESTS):
            payload1 = { "password": f"h00rrahforscience{request}"}
            accepted_requests.append(executor.submit(get_status,endpoint=endpoint, payload=payload1))
        
        # stop server
        executor.submit(stop_server, url=base_url, port=port)

        # requests after app received shutdown signal
        for request in range(REQUESTS):
            payload2 = { "password": f"stoppedserver{request}"}
            not_accepted_requests.append(executor.submit(get_status_error, endpoint=endpoint, payload=payload2))

    for future in concurrent.futures.as_completed(accepted_requests):
        assert(future.result() == 200)

    for future in concurrent.futures.as_completed(not_accepted_requests):
        # validate requests were rejected
        assert("Max retries exceeded" in str(future.result()))
        assert("Connection refused" in str(future.result()))
    