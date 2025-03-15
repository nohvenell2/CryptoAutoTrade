import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote
import dotenv

dotenv.load_dotenv()
access_key = os.environ['OTPYRC_ACC']
secret_key = os.environ['OTPYRC_CES']
server_url = os.environ['SERVER_URL']

def check_order(id):
    params = {
    'uuid': id
    }
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }

    res = requests.get(server_url + '/v1/order', params=params, headers=headers)
    return res.json()

if __name__ == "__main__":
    print(check_order('af38b690-50da-4b5f-a192-1c0440cfb5e8'))
