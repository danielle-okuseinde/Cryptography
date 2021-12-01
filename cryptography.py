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
    # if a and/or b value isn't filled, return error page
    # encryption algorithm
    # make dictionary of what each letter maps to maybe and display that
    # when all is done, render template w dictionary, plaintext, and ciphertext
    if request.method == 'POST':
        plaintext = request.form.get('plaintext')
        plaintext = plaintext.upper()
        a = request.form.get('a')
        b = request.form.get('b')

        if not a.isdigit() or not b.isdigit():
            return render_template('affine.html', error="Your a and b values are invalid. Try again!")
        else:
            ciphertext = affine_encrypt(plaintext, int(a), int(b))
            crib = ciphertext[1]
            ciphertext = ciphertext[0]
            temp = {}
            for key in crib:
                temp[key] = crib[key][1]
            return render_template('affine.html', plaintext=plaintext, ciphertext=ciphertext, crib=temp)

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


def reset_crib():
    crib = {}
    n = 0
    while n <= 90:
        crib[chr(n+65)] = (chr(n+65), n)
    return crib

def affine_encrypt(plaintext, a, b):
    crib = reset_crib()
    for key in crib:
        val = crib[key][1]
        val = (val*a+b)%26
        crib[key] = (chr(val+65), val)
    
    for letter in plaintext:
        letter = crib[letter]
    
    return plaintext, crib

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3001, debug=True)
