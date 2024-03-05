import json
from mitmproxy import http
from Crypto.PublicKey import RSA


def response(flow: http.HTTPFlow) -> None:
    """Intercepts responses from the server"""
    # replace the server's public key with our own
    if flow.request.path == '/pk/' and flow.request.method == 'GET':
        flow.response = http.Response.make(
            200,
            'TODO: replace this string with the public key in PEM format',
            {'content-type': 'text/plain'},
        )
    elif flow.request.path == '/pk_json/' and flow.request.method == 'GET':
        flow.response = http.Response.make(
            200,
            json.dumps({
                'N': 42, # TODO: replace 42 with the modulus N
                'e': 47, # TODO: replace 47 with the public exponent e
            }),
            {'content-type': 'application/json'},
        )
