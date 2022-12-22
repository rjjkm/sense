import argparse
import os
from cryptography.fernet import Fernet

parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store_true',
    help='Save clear text credentials after encrypting. Default is delete files.')
args = parser.parse_args()

# Read clear text username file
with open('.creds/user', 'r') as f:
    user = ''.join(f.readlines())

f = open('.creds/pwd', 'r')
pwd = ''.join(f.readlines())

# Generate key file
key = Fernet.generate_key()
f = open(".creds/key", "wb")
f.write(key)
f.close()

# Encrypt username
crypto = Fernet(key)
secure_user = crypto.encrypt(bytes(user, 'utf-8'))
f = open(".creds/secure-user", "wb")
f.write(secure_user)
f.close()

# Encrypt password
secure_pwd = crypto.encrypt(bytes(pwd, 'utf-8'))
f = open(".creds/secure-pwd", "wb")
f.write(secure_pwd)
f.close()

if not args.s:
    print("Deleting clear text credentials")
    try:
        os.remove(".creds/user")
        os.remove(".creds/pwd")
    except FileNotFoundError:
        pass
