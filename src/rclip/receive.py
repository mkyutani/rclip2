from base64 import b64decode, urlsafe_b64decode
import json
import sys
import requests

from rclip.utils import get_api, get_crypt_key, decrypt

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
    texts = structure['texts']
    crypt_key = get_crypt_key()
    if crypt_key is not None:
        try:
            texts = [decrypt(text, crypt_key) for text in texts]
        except Exception as e:
            print(f'Failed to decrypt: {str(e)}', file=sys.stderr)
            return False
    
    print('\n'.join(texts))
    return True

def receive_file(structure: dict, encoded_filename: str) -> bool:
    filename = urlsafe_b64decode(encoded_filename.encode('utf-8')).decode('utf-8')
    b64data_list = structure['texts']
    
    crypt_key = get_crypt_key()
    if crypt_key is not None:
        try:
            b64data_list = [decrypt(b64data, crypt_key) for b64data in b64data_list]
        except Exception as e:
            print(f'Failed to decrypt: {str(e)}', file=sys.stderr)
            return False
    
    with open(filename, 'wb') as f:
        for b64data in b64data_list:
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