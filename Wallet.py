from tronpy import Tron
from tronpy.keys import PrivateKey
import os
from dotenv import load_dotenv

load_dotenv()

TRX_PRIVATE_KEY = os.getenv("TRX_PRIVATE_KEY")
TRX_ADDRESS = os.getenv("TRX_ADDRESS")

client = Tron()
priv_key = PrivateKey(bytes.fromhex(TRX_PRIVATE_KEY))

def send_trx(to_address, amount):
    """TRX gönderir (amount TRX)"""
    txn = (
        client.trx.transfer(TRX_ADDRESS, to_address, int(amount * 1_000_000))
        .build()
        .sign(priv_key)
    )
    result = txn.broadcast().wait()
    return result

def get_balance(address):
    balance = client.get_account(address).get('balance', 0) / 1_000_000
    return balance
