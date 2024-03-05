import secrets
from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from users import users
import settings
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

app = Flask(__name__)
app.secret_key = settings.secret_key

rsa_private_key = RSA.import_key(settings.rsa_private_key_pem)
rsa_public_key = RSA.import_key(settings.rsa_public_key_pem)


@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print('X' * 80)
        print(f'login: {username=}    {password=}')
        print('X' * 80)
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/view_secrets/')
def view_secrets():
    if 'username' in session:
        return render_template('secrets.html', secret=settings.secret)
    return redirect(url_for('login'))


@app.route('/pk/')
def pk():
    response = make_response(settings.rsa_public_key_pem)
    response.mimetype = "text/plain"
    return response


@app.route('/pk_json/')
def pk_json():
    return {'N': rsa_public_key.n, 'e': rsa_public_key.e}


@app.route('/upload_secrets/', methods=['GET', 'POST'])
def upload_secrets():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            ciphertext = bytes.fromhex(request.form['ciphertext'])
            cipher = PKCS1_OAEP.new(rsa_private_key)
            plaintext = cipher.decrypt(ciphertext)
            print('X' * 80)
            print(f'decrypted: {plaintext=}')
            print('X' * 80)
        except Exception as e:
            return f'something went wrong: {str(e)}'
        return render_template('thanks_for_secrets.html')
    return render_template('upload_secrets.html')
