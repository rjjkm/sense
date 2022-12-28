import argparse
from credentials import *

parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store_false',
    help='Save clear text credentials after encrypting. Default is delete files.')
args = parser.parse_args()

encrypt_user_and_pwd(args.s)
