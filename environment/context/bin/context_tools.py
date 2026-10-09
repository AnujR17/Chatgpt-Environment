#!/usr/bin/env python3
"""Explicit, cached Mem0 fallback; prefer connected MCP tools when available."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import build_opener, HTTPRedirectHandler, Request

STATE_ROOT = Path('/workspace/shared/environment-context/state')
MAX_RESPONSE = 8 * 1024 * 1024
ENVIRONMENT_NAME = 'Chatgpt-Environment'


class SetupError(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SetupError('Redirect rejected; credential headers must stay on the configured host.')


def required(name):
    value = os.environ.get(name)
    if not value:
        raise SetupError(f'{name} is missing. Configure it in environment settings, not chat.')
    return value


def session_id(explicit=None):
    value = explicit or os.environ.get('CODEX_THREAD_ID') or os.environ.get('CODEX_SESSION_ID')
    if not value:
        raise SetupError('A task/session identifier is required; supply --session with a unique task ID.')
    return value


def topic_id(value):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}', value):
        raise SetupError('Topic must be a lowercase slug, for example digital-cheque.')
    return ENVIRONMENT_NAME + '/topic/' + value


def credential_scope():
    # Separate caches when switching actual keys, without storing or printing the key.
    # Proxy-placeholder rotations still need an explicit refresh after configuration changes.
    return hashlib.sha256(required('MEM0_API_KEY').encode()).hexdigest()


def check_text(text, limit):
    text = text.strip()
    if not text or len(text) > limit:
        raise SetupError(f'Provide nonempty text no longer than {limit} characters.')
    for name in ('ENV_ALL', 'MEM0_API_KEY', 'FIGMA_ACCESS_TOKEN', 'FIGMA_TOKEN'):
        value = os.environ.get(name)
        if value and len(value) >= 8 and value in text:
            raise SetupError('Text contains a configured credential; no request was sent.')
    if re.search(r'(?i)(?:api[_ -]?key|access[_ -]?token|password|secret)\s*[:=]\s*\S+', text):
        raise SetupError('Text appears to contain credentials; remove them before sending.')
    return text


def request_json(url, token_variable, header, payload=None):
    # The caller uses fixed service hosts. Proxy settings and verified TLS are inherited.
    token = required(token_variable)
    if '\r' in token or '\n' in token:
        raise SetupError(f'{token_variable} is invalid; update it securely in environment settings.')
    headers = {'Accept': 'application/json', header: ('Token ' + token if header == 'Authorization' else token)}
    data = None
    if payload is not None:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(payload).encode('utf-8')
    request = Request(url, data=data, headers=headers)
    try:
        with build_opener(NoRedirect()).open(request, timeout=20) as response:
            body = response.read(MAX_RESPONSE + 1)
    except HTTPError as error:
        # Do not print response bodies, headers or exception reprs containing credentials.
        raise SetupError(f'HTTP {error.code}; check service access, credential scope and network settings. No automatic retry.') from None
    except (URLError, OSError, TimeoutError):
        raise SetupError('Network request failed; no automatic retry. A write may have reached the service.') from None
    if len(body) > MAX_RESPONSE:
        raise SetupError('Response exceeds the local size limit.')
    try:
        return json.loads(body)
    except (ValueError, UnicodeError):
        raise SetupError('Service returned invalid JSON; no automatic retry.') from None


def cached_request(key, send, refresh=False):
    """Serialize requests and retain outcomes, including failures, to prevent retry storms."""
    digest = hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()
    STATE_ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    cache = STATE_ROOT / (digest + '.json')
    with (STATE_ROOT / (digest + '.lock')).open('a') as lock:
        os.chmod(lock.name, 0o600)
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        if cache.exists():
            result = json.loads(cache.read_text())
            if not refresh or (refresh == 'failed' and result['status'] == 'ok'):
                return {**result, 'cached': True}
        # Record an uncertain attempt BEFORE sending. A killed process must not resend a write.
        pending = {'status': 'error', 'error': 'Previous request outcome is unknown. Diagnose before an explicit retry.', 'cached': False}
        atomic_json(cache, pending)
        try:
            result = {'status': 'ok', 'data': send(), 'cached': False}
        except SetupError as error:
            result = {'status': 'error', 'error': str(error), 'cached': False}
        atomic_json(cache, result)
        return result


def atomic_json(path, data):
    fd, temporary = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(data, stream)
            stream.write('\n')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def start_memory(topic, query, session=None, refresh=False):
    agent = topic_id(topic)
    user = ENVIRONMENT_NAME
    task = session_id(session)
    query = check_text(query, 1500)
    account = credential_scope()  # The API key is the only required configured credential.
    payload = {'query': query, 'filters': {'AND': [{'user_id': user}, {'agent_id': agent}]}, 'top_k': 8}
    # Query is deliberately excluded: one retrieval per topic/task, even if rephrased.
    return cached_request(['mem0-start', account, user, agent, task], lambda: request_json(
        'https://api.mem0.ai/v3/memories/search/', 'MEM0_API_KEY', 'Authorization', payload), refresh)


def save_memory(topic, text, checkpoint, retry=False):
    agent = topic_id(topic)
    user = ENVIRONMENT_NAME
    text = check_text(text, 5000)
    account = credential_scope()
    payload = {
        'messages': [{'role': 'user', 'content': text}],
        'filters': {'user_id': user, 'agent_id': agent},
        'metadata': {'environment': ENVIRONMENT_NAME, 'topic': topic,
                     'checkpoint': checkpoint, 'source': 'AnujR17/Chatgpt-Environment'},
    }
    content_hash = hashlib.sha256(text.encode()).hexdigest()
    # Deduplicate the same text across sessions and checkpoint labels.
    key = ['mem0-save', account, user, agent, content_hash]
    return cached_request(key, lambda: request_json(
        'https://api.mem0.ai/v3/memories/add/', 'MEM0_API_KEY', 'Authorization', payload), 'failed' if retry else False)


def local_status():
    return {'status': 'local-only', 'credentials': {'MEM0_API_KEY': bool(os.environ.get('MEM0_API_KEY'))},
            'environment_entity': ENVIRONMENT_NAME,
            'mem0_topic_isolation': 'environment user_id AND topic-specific agent_id',
            'mem0': 'prefer connected MCP; this helper is the direct-API fallback',
            'figma': 'use connected plugin only; no Figma token setting required'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('status', help='Inspect configuration presence with zero network requests.')
    start = sub.add_parser('mem0-start', help='Retrieve topic context once per task; reuse cached outcomes.')
    start.add_argument('--topic', required=True)
    start.add_argument('--query', required=True)
    start.add_argument('--session')
    start.add_argument('--refresh', action='store_true', help='Explicit extra retrieval after a meaningful change.')
    save = sub.add_parser('mem0-save', help='Save a curated decision or handoff; never a raw transcript.')
    save.add_argument('--topic', required=True)
    save.add_argument('--file', required=True, help='UTF-8 file containing the curated summary.')
    save.add_argument('--checkpoint', choices=('decision', 'correction', 'handoff'), required=True)
    save.add_argument('--retry', action='store_true', help='Explicit resubmission; diagnose uncertain outcomes first.')
    args = parser.parse_args()
    try:
        if args.command == 'status':
            result = local_status()
        elif args.command == 'mem0-start':
            result = start_memory(args.topic, args.query, args.session, args.refresh)
        elif args.command == 'mem0-save':
            if Path(args.file).stat().st_size > 20000:
                raise SetupError('Summary file is too large; send a curated handoff only.')
            result = save_memory(args.topic, Path(args.file).read_text(encoding='utf-8'), args.checkpoint, args.retry)
    except SetupError as error:
        result = {'status': 'blocked', 'error': str(error)}
    except (OSError, ValueError, UnicodeError):
        result = {'status': 'blocked', 'error': 'Local input or cache could not be read; check files without dumping secrets.'}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['status'] in ('ok', 'local-only') else 2


if __name__ == '__main__':
    raise SystemExit(main())
