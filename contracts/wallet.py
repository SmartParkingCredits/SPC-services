from web3 import Web3
import os

class Wallet:

    node_url = os.environ.get("NODE_URL", 'http://127.0.0.1:8545') # 'https://sepolia.infura.io/v3/'
    w3 = Web3(Web3.HTTPProvider(node_url))
    account = w3.eth.account.create()

    def __init__(self) -> None:
        pass

    def address(self) -> str:
        return self.account.address
