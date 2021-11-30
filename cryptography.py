import urllib.request 
import json
from urllib.request import urlopen, Request
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/ciphers', methods=['GET'])
def ciphers():
    return render_template('ciphers.html')

@app.route('/affine', methods=['POST', 'GET'])
def affine():
    if request.method == 'POST':
        pt = request.form['plaintext']
        a = request.form['a']
        b = request.form['b']
       
        # if a and/or b value isn't filled, return error page
        # encryption algorithm
        # make dictionary of what each letter maps to maybe and display that
        # when all is done, render template w dictionary, plaintext, and ciphertext
        pass
    
@app.route('/affine/encryption', methods=['POST', 'GET'])
def affine_encryption():
    pass

@app.route('/caesar', methods=['GET'])
def caesar():
    pass

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
