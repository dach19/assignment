import pytest
from start_stop_server import start_server, stop_server


def pytest_addoption(parser):
    parser.addoption(
        '--base-url', action='store', default='http://127.0.0.1', help='Base URL for the API tests'
    )
    parser.addoption(
        '--port', action='store', default='http://127.0.0.1', help='Base URL for the API tests'
    )


@pytest.fixture(scope="class")
def start_stop_server(request):
	"""
	Fixture to allow pytest to start and stop server and return command line parameters
	"""
	base_url = request.config.getoption("--base-url")
	port =request.config.getoption("--port")
	opt = {
		"base_url": base_url,
		"port": port,
	}

	start_server(port)
	yield  opt
	# Shutdown server
	# curl -X POST -d 'shutdown' http://127.0.0.1:PORT/hash
	stop_server(base_url, port)


@pytest.fixture(scope="class")
def config(request):
	"""
	Fixture to get command line parameters
	"""
	base_url = request.config.getoption("--base-url")
	port =request.config.getoption("--port")
	opt = {
		"base_url": base_url,
		"port": port,
	}
	return opt
