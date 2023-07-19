import flask
from flask import request, jsonify, Flask
from flask_api import status
import os
import requests, json
from flask_httpauth import HTTPBasicAuth
from auth import packLink, signK1, parseLink, generatePrivateKey

auth = HTTPBasicAuth()
app = Flask(__name__)

# FOR NOW, just using basic auth from users envvar
USER_DATA={
}
usersEnv = os.getenv("users")
if usersEnv != None:
    userinfo = usersEnv.split(",")
    for ui in userinfo:
        parts = ui.split(":")
        if len(parts) == 2:
            USER_DATA[parts[0]] = parts[1]
            print(f'Added user: {parts[0]} to valid users to leverage this endpoint')

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

@app.route("/authenticate", methods = ['POST'])
@auth.login_required
def authenticate():
    # here we want to get the value of user (i.e. ?user=some-value)
    if request.method == 'POST':
        data = request.form
        if request.is_json:
            content = request.get_json()
            make_all_keys_lowercase(content)
            if 'lnurl' in content and 'key' in content:
                http, host, k1 = parseLink(content['lnurl'])
                pub, sig = signK1(content['key'], k1)
                url = packLink(http, host, k1, sig, pub)
                return url, status.HTTP_200_OK
            else:
                return "Your JSON should have a 'lnurl' key/value.", status.HTTP_400_BAD_REQUEST
        else:
            return "You should have 'Content-Type: application/json' added to your header.", status.HTTP_400_BAD_REQUEST

@app.route("/generatePrivateKey", methods = ['GET'])
@auth.login_required
def generateKey():
    # here we want to get the value of user (i.e. ?user=some-value)
    if request.method == 'GET':
        return generatePrivateKey(), status.HTTP_200_OK

def make_all_keys_lowercase(d: dict) -> None:
    for k, v in list(d.items()):
        if type(v) == dict:
            make_all_keys_lowercase(d[k])
        d[k.lower()] = d.pop(k)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8511)