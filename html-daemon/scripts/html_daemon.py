#!/usr/bin/env python3
"""Dependency-free client for the HTML Daemon API. No automatic write retries."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

DEFAULT_URL = 'https://admin.111416.xyz'
MAX_BYTES = 1048576

def request(base, method, path, data=None, headers=None, raw=False):
    req = Request(base + path, data=data, headers={'User-Agent': 'HTMLDaemonClient/1.0', **(headers or {})}, method=method)
    with urlopen(req, timeout=30) as response:
        body = response.read()
        return body if raw else json.loads(body) if body else None

def file_bytes(path):
    if path.suffix.lower() != '.html':
        raise ValueError('Choose a .html file.')
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('HTML exceeds the 1 MiB limit.')
    data = path.read_bytes()
    text = data.decode('utf-8')
    if not text.strip() or '\0' in text:
        raise ValueError('HTML must be nonempty UTF-8 without NUL bytes.')
    return data, text

def verified(base, doc, data):
    expected = hashlib.sha256(data).hexdigest()
    actual = request(base, 'GET', doc['downloadUrl'], raw=True)
    if doc['contentSha256'] != expected or hashlib.sha256(actual).hexdigest() != expected:
        raise ValueError('Document was saved but verification failed. Inspect its current version before retrying.')
    return dict(doc, verified=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default=os.environ.get('HTML_DAEMON_URL', DEFAULT_URL))
    subs = parser.add_subparsers(dest='command', required=True)
    upload = subs.add_parser('upload'); upload.add_argument('file', type=Path); upload.add_argument('--title')
    listing = subs.add_parser('list'); listing.add_argument('--search', default=''); listing.add_argument('--cursor'); listing.add_argument('--limit', type=int, default=25)
    subs.add_parser('get').add_argument('id')
    download = subs.add_parser('download'); download.add_argument('id'); download.add_argument('output', type=Path)
    replace = subs.add_parser('replace'); replace.add_argument('id'); replace.add_argument('file', type=Path); replace.add_argument('--version', type=int, required=True)
    rename = subs.add_parser('rename'); rename.add_argument('id'); rename.add_argument('--title'); rename.add_argument('--filename'); rename.add_argument('--version', type=int, required=True)
    delete = subs.add_parser('delete'); delete.add_argument('id'); delete.add_argument('--version', type=int, required=True)
    args = parser.parse_args()
    base = args.base_url.rstrip('/')
    parsed = urlparse(base)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.query or parsed.fragment or parsed.path:
        parser.error('--base-url must be an HTTP(S) origin.')
    if hasattr(args, 'version') and args.version < 1:
        parser.error('--version must be a positive integer.')
    if hasattr(args, 'id') and not re.fullmatch(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}', args.id):
        parser.error('Provide a lowercase UUIDv4 document ID.')
    path = '/v1/documents/' + getattr(args, 'id', '')
    headers = {'If-Match': '"%s"' % args.version} if hasattr(args, 'version') else {}
    if args.command == 'upload':
        data, text = file_bytes(args.file)
        body = json.dumps({'title': args.title or args.file.stem, 'filename': args.file.name, 'html': text}).encode('utf-8')
        doc = request(base, 'POST', '/v1/documents', body, {'Content-Type': 'application/json'})
        # Print the saved identity even if a later verification request fails.
        print(json.dumps({'savedId': doc['id'], 'version': doc['version']}, ensure_ascii=False), file=sys.stderr)
        result = verified(base, doc, data)
    elif args.command == 'list':
        query = {'limit': args.limit, 'search': args.search}
        if args.cursor: query['cursor'] = args.cursor
        result = request(base, 'GET', '/v1/documents?' + urlencode(query))
    elif args.command == 'get':
        result = request(base, 'GET', path)
    elif args.command == 'download':
        data = request(base, 'GET', path + '/content', raw=True)
        # Avoid silently overwriting an existing local file.
        with args.output.open('xb') as output: output.write(data)
        result = {'path': str(args.output), 'sizeBytes': len(data), 'contentSha256': hashlib.sha256(data).hexdigest()}
    elif args.command == 'replace':
        data, _ = file_bytes(args.file); headers['Content-Type'] = 'text/html; charset=utf-8'
        doc = request(base, 'PUT', path + '/content', data, headers)
        print(json.dumps({'savedId': doc['id'], 'version': doc['version']}), file=sys.stderr)
        result = verified(base, doc, data)
    elif args.command == 'rename':
        body = {key: value for key, value in [('title', args.title), ('filename', args.filename)] if value is not None}
        if not body: parser.error('Provide --title or --filename.')
        headers['Content-Type'] = 'application/json'
        result = request(base, 'PATCH', path, json.dumps(body).encode('utf-8'), headers)
    else:
        request(base, 'DELETE', path, headers=headers); result = {'id': args.id, 'deleted': True}
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try: main()
    except HTTPError as error:
        print('HTTP %s: %s' % (error.code, error.read().decode('utf-8', errors='replace')), file=sys.stderr); sys.exit(1)
    except (ValueError, OSError, URLError) as error:
        print(str(error), file=sys.stderr); sys.exit(1)
