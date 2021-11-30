import urllib.request 
import json
from urllib.request import urlopen, Request
import flask
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def ciphers():
    return render_template('cryptography.html')

@app.route('/affine', methods=['POST', 'GET'])
def affine():
    if request.method == 'POST':
        plaintext = request.form.get('plaintext')
        print(plaintext)
        ciphertext=""
        return render_template('affine.html', plaintext=plaintext, ciphertext=ciphertext)

    return render_template('affine.html')

@app.route('/affine/encryption', methods=['POST', 'GET'])
def affine_encryption():
    pass

@app.route('/caesar', methods=['GET'])
def caesar():
    return 'Caesar'

@app.route('/vigenere', methods=['GET'])
def vigenere():
    pass

@app.route('/aristocrat', methods=['GET'])
def aristocrat():
    pass

@app.errorhandler(404)
def err_404(e):
    return "Couldn't find page", 404

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3001)
