import json
import sys
import requests

def register_message_id(category: str, ttl: int=None) -> str:
    headers = {}

    uri = 'http://localhost/api/v2/messages'
    options = []
    if category is not None:
        options.append(f'category={category}')
    if ttl is not None:
        options.append(f'ttl={ttl}')
    query = '?'.join([uri, '&'.join(options)])

    res = None
    try:
        res = requests.post(query, headers=headers)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return None

    site = json.loads(res.text)
    id = str(site['id'])

    message = ' '.join([str(res.status_code), id])
    print(f'{message} ', file=sys.stderr)

    return id

def send_contents(id: str, contents: list[str]) -> bool:
    headers = { 'Content-Type': 'application/json' }
    query = f'http://localhost/api/v2/messages/{id}'
    data = json.dumps({
        'texts': contents
    })

    res = None
    try:
        res = requests.put(query, headers=headers, data=data)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return False

    if res.status_code >= 400:
        message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
        print(f'{message} ', file=sys.stderr)
        return False

    message = ' '.join([str(res.status_code), res.text if res.text is not None else ''])
    print(f'{message} ', file=sys.stderr)

    return True

def send_text(text: str, ttl: int) -> bool:
    id = register_message_id(category='text', ttl=ttl)
    if id is None:
        return False

    status = send_contents(id, [text])
    if status is False:
        return False

    return True

def send_file(file: str) -> bool:
    print('Not implemented', file=sys.stderr)
    return False

def send(text: str=None, file: str=None, ttl: int=None) -> bool:
    if text is not None:
        status = send_text(text, ttl=ttl)
    elif file is not None:
        status = send_file(file, ttl=ttl)

    return status