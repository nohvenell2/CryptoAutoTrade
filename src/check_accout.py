import jwt
import hashlib
import os
import uuid
from urllib.parse import urlencode, unquote
import requests
import dotenv

dotenv.load_dotenv()

access_key = os.environ['OTPYRC_ACC']
secret_key = os.environ['OTPYRC_CES']
server_url = os.environ['SERVER_URL']
def check_account():
  payload = {
      'access_key': access_key,
      'nonce': str(uuid.uuid4()),
  }

  jwt_token = jwt.encode(payload, secret_key)
  authorization = 'Bearer {}'.format(jwt_token)
  headers = {
    'Authorization': authorization,
  }

  res = requests.get(server_url + '/v1/accounts', headers=headers)
  return res.json()

if __name__ == '__main__':
  result = check_account()
  print(result)

