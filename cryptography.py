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
        a = request.form.get('a')
        b = request.form.get('b')
        temp = {}

        if not a.isdigit() or not b.isdigit() or a%1 == 0 or b%1 == 0:
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
    # maybe change tuple of crib since i could always cast it
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
        else:
            ciphertext+=letter
    
    return ciphertext, crib

@app.route('/caesar', methods=['POST', 'GET'])
def caesar():
    # shift
    # idea: add radio inputs to switch from encrypt to decrypt
      if request.method == 'POST':
        plaintext = request.form.get('plaintext')
        plaintext = plaintext.upper()
        shift = request.form.get('shift')
        temp = {}

        if not shift.isdigit() or not shift%1 == 0:
            return render_template('caesar.html', error="Your shift value is invalid. Try again!")
        else:
            if request.POST['action'] == 'encrypt':
                ciphertext = caesar_cipher(plaintext, shift, True)
                crib = ciphertext[1]
                ciphertext = ciphertext[0]

            elif request.POST['action'] == 'decrypt':
                ciphertext = plaintext
                plaintext = caesar_cipher(plaintext, shift, False)
                crib = plaintext[1]
                plaintext = plaintext[0]

            for key in crib:
                temp[key] = crib[key][0]
                

            return render_template('caesar.html', plaintext="Plaintext: "+plaintext, ciphertext="Ciphertext: "+ciphertext, crib=temp)

        # huh
        # this is for radio inputs later; need to work out logic
        if request.POST['action'] == 'decrypt':
             return render_template('caesar.html', decrypt=True)

        if len(request.form.get('plaintext')) > 0:
            pass # if theres something in the form submitted we need to render template for ec and answer

        if len(request.form.get('ciphertext')) > 0:
            pass # if theres something in the form submitted we need to render template for dc and answer

        else:
            return render_template('caesar.html', encrypt=True)

def caesar_cipher(plaintext, shift, encrypt):
    # maybe change tuple of crib since i could always cast it
    crib = reset_crib()
    for key in crib:
        val = crib[key][1]

        if encrypt:
            val = val+shift
        elif not encrypt:
            val = val-shift

        crib[key] = (chr(val+65), val)
    
    array = [x for x in plaintext]
    
    ciphertext = ""

    for letter in array:
        if letter in crib:
            ciphertext+=crib[letter][0]
        else:
            ciphertext+=letter
    
    return ciphertext, crib


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
