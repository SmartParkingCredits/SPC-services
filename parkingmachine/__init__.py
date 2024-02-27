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
    car_entered_filter = parking_lot.events.CarEntered.createFilter(fromBlock="latest")
    car_exited_filter = parking_lot.events.CarExited.createFilter(fromBlock="latest")

    while True:
        for carEnteredEvent in car_entered_filter.get_new_entries():
            handle_car_entered(carEnteredEvent)
        for carExitedEvent in car_exited_filter.get_new_entries():
            handle_car_exited(carExitedEvent)

def handle_car_entered(event):
    print("Car entered: ", event)

def handle_car_exited(event):
    print("Car exited: ", event)


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
    tx_hash = ParkingLot.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    address = tx_receipt.contractAddress
    print("Smart contract deployed successfully!")
    print("Contract address: ", address)
    return address
