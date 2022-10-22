import base64
import requests
import pytest
from constants import ENDPOINT_STATS, ENDPOINT_HASH, REQUEST_TIMEOUT


@pytest.mark.usefixtures("start_stop_server", "config")
class TestHash:

    # TODO: setup to start server and share parameters between tests

    def test_app_only_accepts_requests_on_specified_port_endpoint_stats(self, config):
        """
        Test app only accepts requests from non specified ports 
        HTTP Method: GET
        Endpoint: /stats
        """
        LOCAL_PORT = 1234
        with pytest.raises(requests.exceptions.ConnectionError) as e_info:
            requests.get(f"{config['base_url'] }:{LOCAL_PORT}/{ENDPOINT_STATS}", timeout=REQUEST_TIMEOUT)
        
        assert("Max retries exceeded" in str(e_info.value))
        assert(f"port={LOCAL_PORT}" in str(e_info.value))

    def test_app_only_accepts_requests_on_specified_port_endpoint_hash(self, config):
        """
        Test app doesn't accept requests from non specified ports 
        HTTP Method: GET
        Endpoint: /hash
        """
        LOCAL_PORT = 1234
        payload = { "password": "angrymonkey"}
        with pytest.raises(requests.exceptions.ConnectionError) as e_info:
            requests.post(f"{ config['base_url'] }:{LOCAL_PORT}/{ENDPOINT_HASH}",
                json=payload,
                timeout=REQUEST_TIMEOUT)

        assert("Max retries exceeded" in str(e_info.value))
        assert(f"port={LOCAL_PORT}" in str(e_info.value))

    def test_app_returns_job_identifier(self, config):
        """
        Test app returns job identifier
        HTTP Method: POST
        Endpoint: /hash
        """
        base_url = config['base_url']
        port = config['port']
        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}"
        payload = { "password": "angrymonkey"}
        r = requests.post(endpoint, json=payload, timeout=REQUEST_TIMEOUT)
        assert(r.status_code == 200)
        assert(int(r.text) > 0)

    def test_app_doesnt_return_encoded_password_for_invalid_job_identifier_string(self, config):
        """
        Test app doesn't return encoded password for invalid job identifier
        HTTP Method: GET
        Endpoint: /hash
        Job Identifier: abcd
        """
        job_identifier = "abcd"
        base_url = config['base_url']
        port = config['port']
        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}/{job_identifier}"
        r = requests.get(endpoint)
        assert(r.status_code == 400)
        assert("invalid syntax" in r.text )

    def test_app_doesnt_return_job_identifier_for_invalid_job_identifier_negative_number(self, config):
        """
        Test app doesn't return encoded passwot for invalid job identifier
        HTTP Method: GET
        Endpoint: /hash
        Job identifier: -123
        """
        job_identifier = -123
        base_url = config['base_url']
        port = config['port']
        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}/{job_identifier}"
        r = requests.get(endpoint)
        assert(r.status_code == 400)
        assert("Hash not found" in r.text )

    def test_app_returns_encoded_password_for_valid_job_identifier(self, config):
        """
        Test app returns encoded password for valid job identifier
        HTTP Method: GET
        Endpoint: /hash
        """
        base_url = config["base_url"]
        port = config["port"]
        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}"
        payload = { "password": "angrymonkey"}
        r = requests.post(endpoint, json=payload, timeout=REQUEST_TIMEOUT)

        job_identifier = int(r.text)
        assert(r.status_code == 200)

        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}/{job_identifier}"
        r = requests.get(endpoint)
        t = r.text.split("/")[-1]
        removed = t.split("==")[0]
        assert(r.status_code == 200)
        assert(base64.b64encode(base64.b64decode(removed)) == removed.encode("ASCII"))

    def test_app_doesnt_accept_delete_method_hash_endpoint(self, config):
        """
        Test app handles not supported HTTP method
        HTTP Method: delete
        Endpoint: /hash
        """
        base_url = config["base_url"]
        port = config["port"]
        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}"
        payload = { "password": "angrymonkey"}
        r = requests.post(endpoint, json=payload, timeout=REQUEST_TIMEOUT)
        job_identifier = int(r.text)
        assert(r.status_code == 200)

        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}/{job_identifier}"
        r = requests.delete(endpoint)
        assert(r.status_code == 405)
        assert("DELETE Not Supported" in r.text)

    def test_app_doesnt_accept_put_method_hash_endpoint(self, config):
        """
        Test app handles not supported HTTP method
        HTTP Method: PUT
        Endpoint: /hash
        """
        base_url = config['base_url']
        port = config['port']
        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}"
        payload = { "password": "angrymonkey"}
        r = requests.put(endpoint, json=payload, timeout=REQUEST_TIMEOUT)

        assert(r.status_code == 405)
        assert("PUT Not Supported" in r.text)

    def test_app_doesnt_accept_patch_method_hash_endpoint(self, config):
        """
        Test app handles not supported HTTP method
        HTTP Method: PATCH
        Endpoint: /hash
        """
        base_url = config['base_url']
        port = config['port']
        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}"
        payload = { "password": "angrymonkey"}
        r = requests.post(endpoint, json=payload, timeout=REQUEST_TIMEOUT)
        job_identifier = int(r.text)
        assert(r.status_code == 200)

        endpoint = f"{base_url}:{port}/{ENDPOINT_HASH}/{job_identifier}"
        r = requests.patch(endpoint)
        assert(r.status_code == 405)
        assert("PATCH Not Supported" in r.text)
