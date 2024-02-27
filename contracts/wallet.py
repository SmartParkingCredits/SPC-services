from web3 import Web3

class Wallet:

    sepolia_url = 'https://sepolia.infura.io/v3/'
    w3 = Web3(Web3.HTTPProvider(sepolia_url))
    account = w3.eth.account.create()

    def __init__(self) -> None:
        pass

    def address(self) -> str:
        return self.account.address
