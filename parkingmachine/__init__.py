from contracts.wallet import Wallet
from contracts import parking_lot_contract
from web3 import Web3
from solcx import compile_source

def run_service(contract_address):
    print("Service running")
    wallet = Wallet()
    account = wallet.account
    w3 = wallet.w3
    parking_lot = parking_lot_contract(w3, contract_address)
    state = float(w3.eth.get_balance(contract_address))
    print("Contract address: ", parking_lot.address)
    while True:
        balance = float(w3.eth.get_balance(contract_address))
        if balance > state:
            handle_car_entered()
        elif balance < state:
            handle_car_exited()
        state = balance


def handle_car_entered():
    print("Car entered: ")

def handle_car_exited():
    print("Car exited: ")


def deploy_contract():
    """
    Function to handle the deployment logic.
    You can add your deployment code here.
    """
    print("Deploying the smart contract...")

    file = open('./contracts/ParkingLot.sol', 'r')
    contract_src = file.read()
    file.close()

    compiled_sol = compile_source(
        contract_src,
        output_values=['abi', 'bin']
    )

    contract_id, contract_interface = compiled_sol.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    wallet = Wallet()
    account = wallet.account
    w3 = wallet.w3

    # Set up your account
    w3.eth.default_account = account.address  # Use one of the Ganache accounts or your testnet account

    # Deploy the contract
    ParkingLot = w3.eth.contract(abi=abi, bytecode=bytecode)
    estimated_gas = ParkingLot.constructor().estimate_gas()

    # Prepare the transaction
    transaction = {
        'from': wallet.account.address,
        'gas': estimated_gas,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(wallet.account.address),
    }

    # Sign and send the transaction
    tx_hash = wallet.sign_and_send_transaction(ParkingLot.constructor().build_transaction(transaction))
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    address = tx_receipt.contractAddress
    print("Smart contract deployed successfully!")
    print("Contract address: ", address)
    return address
