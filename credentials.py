import os
from cryptography.fernet import Fernet

def encrypt_user_and_pwd(delete_unsecure_creds=True):

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

    if delete_unsecure_creds:
        print("Deleting clear text credentials")
        try:
            os.remove(".creds/user")
            os.remove(".creds/pwd")
        except FileNotFoundError:
            pass

def decrypt_user_and_pwd():
    with open('.creds/key') as f:
        key = bytes(''.join(f.readlines()), 'utf-8')
    f.close()

    with open('.creds/secure-user') as f:
        secure_user = bytes(''.join(f.readlines()), 'utf-8')
    f.close()

    with open('.creds/secure-pwd') as f:
        secure_pwd = bytes(''.join(f.readlines()), 'utf-8')
    f.close()

    crypto = Fernet(key)
    return crypto.decrypt(secure_user), crypto.decrypt(secure_pwd)
