import os
import requests
import subprocess
from constants import ENDPOINT_HASH


def start_server(port):
  os.environ['PORT'] = port
  subprocess.Popen("/usr/local/bin/broken-hashserve", stdin = subprocess.PIPE, stdout = subprocess.PIPE)

def stop_server(url, port):
  requests.post(f"{url}:{port}/{ENDPOINT_HASH}", data="shutdown")
