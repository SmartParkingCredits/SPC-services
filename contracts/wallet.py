from web3 import Web3
import os
from dotenv import load_dotenv

class Wallet:

    node_url = os.environ.get("NODE_URL", 'http://127.0.0.1:8545') # 'https://sepolia.infura.io/v3/'
    w3 = Web3(Web3.HTTPProvider(node_url))
    account = w3.eth.account.create()

    def __init__(self) -> None:
        load_dotenv()
        self.node_url = os.environ.get("NODE_URL", 'http://127.0.0.1:8545') # 'https://sepolia.infura.io/v3/'
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))
        print("node url", self.node_url)
        mnemonic = os.environ.get("MNEMONIC")
        if mnemonic:
            self.w3.eth.account.enable_unaudited_hdwallet_features()
            self.account = self.w3.eth.account.from_mnemonic(mnemonic)
            print("loaded account from mnemonic", self.account.address)

    def sign_and_send_transaction(self, transaction):
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.account._private_key)
        return self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    def address(self) -> str:
        return self.account.address
