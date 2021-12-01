import urllib.request 
import json
from urllib.request import urlopen, Request
import flask
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
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
        ciphertext = "test"
        a = request.form.get('a')
        b = request.form.get('b')
        temp = {}

        if not a.isdigit() or not b.isdigit():
            return render_template('affine.html', error="Your a and b values are invalid. Try again!")
        else:
            ciphertext = affine_encrypt(plaintext, int(a), int(b))
            crib = ciphertext[1]
            ciphertext = ciphertext[0]
            for key in crib:
                temp[key] = crib[key][0]

            return render_template('affine.html', plaintext="Plaintext: "+plaintext, ciphertext="Ciphertext: "+ciphertext, crib=temp)

    return render_template('affine.html')

def affine_encrypt(plaintext, a, b):
    crib = reset_crib()
    for key in crib:
        val = crib[key][1]
        val = (val*a+b)%26
        crib[key] = (chr(val+65), val)
    
    array = [x for x in plaintext]
    
    ciphertext = ""

    for letter in array:
        if letter in crib:
            ciphertext+=crib[letter][0]
    
    return ciphertext, crib

@app.route('/caesar', methods=['GET'])
def caesar():
    return 'Caesar'

@app.route('/vigenere', methods=['GET'])
def vigenere():
    pass

@app.route('/aristocrat', methods=['GET'])
def aristocrat():
    pass

def reset_crib():
    crib = {}
    n = 0
    for n in range(26):
        crib[chr(n+65)] = (chr(n+65), n)
    return crib

@app.errorhandler(404)
def err_404(e):
    return "Couldn't find page", 404


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3001, debug=True)
