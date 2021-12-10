import urllib.request 
import json
from urllib.request import urlopen, Request
import flask
from flask import Flask, render_template, request
import random
from random import shuffle

app = Flask(__name__)

global encrypt

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/affine', methods=['POST', 'GET'])
def affine():
    if request.method == 'POST':
        plaintext = request.form.get('plaintext')
        plaintext = plaintext.upper()
        a = request.form.get('a')
        b = request.form.get('b')
        temp = {}

        if not a.isdigit() or not b.isdigit() or not(float(a)%1 == 0 or float(b)%1 == 0):
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

# PLZZ FIX
@app.route('/caesar', methods=['POST', 'GET'])
def caesar():
    # shift
    # idea: add radio inputs to switch from encrypt to decrypt 
    if request.method == 'POST':
        if request.form.get('encrypt-or-decrypt') == 'Decrypt':
            return render_template('caesar.html', decrypt=True)

        elif request.form.get('encrypt-or-decrypt') == 'Encrypt':
            return render_template('caesar.html', encrypt=True)

        else:
            global encrypt
            encrypt = True
            ready = False
            if not request.form.get('plaintext') == None:
                plaintext = request.form.get('plaintext')
                ready = True
            elif not request.form.get('ciphertext') == None:
                plaintext = request.form.get('ciphertext')
                encrypt = False
                ready = True

            if ready:
                plaintext = plaintext.upper()

                shift = request.form.get('shift')
                temp = {}

                if not shift.isdigit() or not float(shift)%1 == 0:
                    if encrypt: 
                        return render_template('caesar.html', error="Your shift value is invalid. Try again!", encrypt=True)
                    else:
                        return render_template('caesar.html', error="Your shift value is invalid. Try again!", decrypt=True)
            
                else:
                    if encrypt:
                        ciphertext = caesar_cipher(plaintext, int(shift), True)
                        crib = ciphertext[1]
                        ciphertext = ciphertext[0]

                        for key in crib:
                            temp[key] = crib[key][0]

                    elif not encrypt:
                        ciphertext = plaintext
                        plaintext = caesar_cipher(plaintext, int(shift), False)
                        crib = plaintext[1]
                        plaintext = plaintext[0]

                        for key in crib:
                            temp[key] = crib[key][0]
                        
                    if encrypt:
                        return render_template('caesar.html', plaintext="Plaintext: "+plaintext, ciphertext="Ciphertext: "+ciphertext, crib=temp, encrypt=True)
                    elif not encrypt:
                        return render_template('caesar.html', plaintext="Plaintext: "+plaintext, ciphertext="Ciphertext: "+ciphertext, crib=temp, decrypt=True)

    return render_template('caesar.html', encrypt=True)

def caesar_cipher(plaintext, shift, encrypt):
    # maybe change tuple of crib since i could always cast it
    crib = reset_crib()
    for key in crib:
        val = crib[key][1]

        if encrypt:
            val = (val+shift)%26
        elif not encrypt:
            val = (val-shift)%26

        crib[key] = (chr(val+65), val)
    
    array = [x for x in plaintext]
    
    ciphertext = ""

    for letter in array:
        if letter in crib:
            ciphertext+=crib[letter][0]
        else:
            ciphertext+=letter
    
    return ciphertext, crib


@app.route('/vigenere', methods=['POST', 'GET'])
def vigenere(): 
    if request.method == 'POST':
        if request.form.get('encrypt-or-decrypt') == 'Decrypt':
            return render_template('vigenere.html', decrypt=True)

        elif request.form.get('encrypt-or-decrypt') == 'Encrypt':
            return render_template('vigenere.html', encrypt=True)

        else:
            global encrypt
            encrypt = True
            ready = False
            if not request.form.get('plaintext') == None:
                encrypt = True
                plaintext = request.form.get('plaintext')
                ready = True
            elif not request.form.get('ciphertext') == None:
                encrypt = False
                plaintext = request.form.get('ciphertext')
                ready = True

            if ready:
                plaintext = plaintext.upper()
                key = request.form.get('key')

                if key == None:
                    return render_template('vigenere.html', error="Please enter a key.")
                elif not valid_key(key):
                    return render_template('vigenere.html', error="Your keyword is invalid. No special characters or numbers. Try again!")
            
                else:
                    key = key.upper()
                    if encrypt:
                        ciphertext = vigenere_cipher(plaintext, key, True)

                    elif not encrypt:
                        ciphertext = plaintext
                        plaintext = vigenere_cipher(plaintext, key, False)
                    
                    if encrypt:
                        return render_template('vigenere.html', plaintext="Plaintext: "+plaintext, ciphertext="Ciphertext: "+ciphertext, encrypt=True)
                    elif not encrypt:
                        return render_template('vigenere.html', plaintext="Plaintext: "+plaintext, ciphertext="Ciphertext: "+ciphertext, decrypt=True)

    return render_template('vigenere.html', encrypt=True)

def vigenere_cipher(plaintext, key, en):
    key = split(key)
    ciphertext = ""
    x = 0
    if en:
        for letter in plaintext:
            num = ord(letter)-65
            if num >= 0 and num <= 25:
                num = (num + (ord(key[x%len(key)])-65))%26
            ciphertext+=chr(num+65)
            x+=1

    elif not en:
        for letter in plaintext:
            num = ord(letter)-65
            if num >= 0 and num <= 25:
                num = (num - (ord(key[x%len(key)])-65))%26
            ciphertext+=chr(num+65)
            x+=1
    return ciphertext


def valid_key(key):
    key = key.upper()
    for letter in key:
        num = ord(letter)
        if not (num >= 65 and num <= 90):
            return False
    return True

def split(word):
    return [char for char in word]

@app.route('/aristocrat', methods=['POST','GET'])
def aristocrat():
    if request.method == 'POST':
        plaintext = request.form.get('plaintext')
        plaintext = plaintext.upper()
        temp = {}

        if plaintext == " " or plaintext == None:
            return render_template('arisocrat.html', error="Input something in the plaintext please!")
        else:
            ciphertext = generate_aristocrat(plaintext)
            crib = ciphertext[1]
            ciphertext = ciphertext[0]
            for key in crib:
                temp[key] = crib[key][0]

            return render_template('aristocrat.html', plaintext="Plaintext: "+plaintext, ciphertext="Ciphertext: "+ciphertext, crib=temp)

    return render_template('aristocrat.html')

 
def generate_aristocrat(plaintext):
    crib = randomize_crib()
    array = [x for x in plaintext]
    
    ciphertext = ""

    for letter in array:
        if letter in crib:
            ciphertext+=crib[letter][0]
        else:
            ciphertext+=letter
    
    return ciphertext, crib

def randomize_crib():
    temp = []
    crib = reset_crib()
    for x in range(26):
        temp.append(x)
    
    shuffle(temp)

    # basically go through and assign each letter key to corresponding temp crib value and remember to also add the letter values
    x = 0
    for key in crib:
        crib[key] = (chr(temp[x]+65), temp[x])
        x+=1
    
    return crib
    

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
