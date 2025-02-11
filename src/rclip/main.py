import argparse
import io
import signal
import sys

from rclip import flush, ping, receive, send
from rclip.utils import generate_crypt_key

def setup():
    signal.signal(signal.SIGINT, lambda num, frame: sys.exit(1))
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=False)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=False)

def main() -> int:
    setup()

    parser = argparse.ArgumentParser(description='Remote Clip Client')
    parser.add_argument('key', nargs='?', type=str, metavar='KEY|ping|generate|flush', default=None, help='Key to receive data, ping, generate key or flush server data')
    parser.add_argument('-T', '--ttl', type=int, default=None, help='Time to live for the message')
    input_type = parser.add_mutually_exclusive_group()
    input_type.add_argument('-f', '--file', type=str, help='File to send')
    input_type.add_argument('-t', '--text', type=str, help='Text to send')
    args = parser.parse_args()

    if args.key is None:
        if args.file is not None:
            status = send(file=args.file, ttl=args.ttl)
        else:
            if args.text is None:
                text = sys.stdin.read()
            else:
                text = args.text
            status = send(text=text, ttl=args.ttl)
    else:
        if args.key.lower() == 'ping':
            result = ping()
            if result is not None:
                print(result)
                status = True
            else:
                status = False
        elif args.key.lower() == 'generate':
            key = generate_crypt_key()
            print(key)
            status = True
        elif args.key.lower() == 'flush':
            status = flush()
        else:
            status = receive(args.key)

    return 0 if status else 1

if __name__ == '__main__':
    sys.exit(main())