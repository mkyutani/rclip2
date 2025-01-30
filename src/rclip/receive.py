from base64 import b64decode, urlsafe_b64decode
import json
import sys
import requests

from rclip.utils import get_api

def get_structure(key: str) -> dict:
    headers = {}
    query = get_api(f'/api/v2/messages/{key}')

    res = None
    try:
        res = requests.get(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    structure = json.loads(res.text)

    return structure

def receive_text(structure: dict) -> bool:
    print('\n'.join(structure['texts']))
    return True

def receive_file(structure: dict, encoded_filename: str) -> bool:
    filename = urlsafe_b64decode(encoded_filename.encode('utf-8')).decode('utf-8')
    with open(filename, 'wb') as f:
        for b64data in structure['texts']:
            f.write(b64decode(b64data.encode('utf-8')))

    return True

def receive(key: str) -> bool:
    structure = get_structure(key)
    if structure is None:
        return False
    elif structure['category'] == 'text':
        return receive_text(structure)
    elif structure['category'].startswith('file:'):
        return receive_file(structure, structure['category'][5:])
    else:
        print('Unknown category', file=sys.stderr)
        return False