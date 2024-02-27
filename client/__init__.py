from contracts.wallet import Wallet
from contracts import parking_lot_contract
from web3 import Web3

from .qrcodereader import *

def enter(address: str, value):
    wallet = Wallet()
    account = wallet.account
    w3 = wallet.w3
    parking_lot = parking_lot_contract(w3, address)
    value_wei = w3.to_wei(value, 'ether')
    tx = parking_lot.functions.enter().transact({'from': account.address, 'value': int(value_wei)})
    print(f"Transaction hash: {tx.hex()}")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx)
    print(f"Block hash: {tx_receipt.blockHash.hex()}")
    print(f"Transaction included in block: {tx_receipt.blockNumber}")
    return tx, tx_receipt
