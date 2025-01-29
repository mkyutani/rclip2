import json
import sys
import requests

def ping() -> str:
    headers = {}

    res = None
    try:
        res = requests.get('http://localhost/api/v2/ping', headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    result = json.loads(res.text)
    if 'message' not in result:
        return None
    else:
        return result['message']