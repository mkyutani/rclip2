from base64 import b64decode
import json
import sys
import requests

from rclip.utils import get_api

def flush() -> bool:
    headers = {}
    query = get_api('/api/v2/messages')

    res = None
    try:
        res = requests.delete(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return False

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return False

    return True