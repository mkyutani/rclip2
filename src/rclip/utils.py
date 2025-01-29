import os
from urllib.parse import urljoin

def get_api(dir: str) -> str:
    server = os.environ.get('RCLIP_API', 'http://localhost:8099')
    return urljoin(server, dir)