from contracts.wallet import Wallet
from contracts import parking_lot_contract
from web3 import Web3
from solcx import compile_source
from .servo import Servo
import os
import time

def run_service(contract_address):
    print("Service running")
    wallet = Wallet()
    account = wallet.account
    w3 = wallet.w3
    parking_lot = parking_lot_contract(w3, contract_address)

    print("Contract address: ", parking_lot.address)

    balance = float(w3.eth.get_balance(contract_address))
    print(f"Contract balance: {balance}")

    prev_entered = parking_lot.functions.totalCarsEntered().call()
    prev_left = parking_lot.functions.totalCarsLeft().call()

    print(f"Initial state: {prev_entered} cars entered, {prev_left} cars left")

    while True:
        # Check current states
        current_entered = parking_lot.functions.totalCarsEntered().call()
        current_left = parking_lot.functions.totalCarsLeft().call()

        # Detect changes
        if current_entered > prev_entered:
            handle_car_entered()
            prev_entered = current_entered  # Update the previous state

        if current_left > prev_left:
            handle_car_exited()
            prev_left = current_left  # Update the previous state


def handle_car_entered():
    print("Car entered: ")
    port = os.getenv('SERVO_PORT')
    servo = Servo(port)
    servo.connect()
    servo.move_servo(90)
    time.sleep(4)
    servo.move_servo(45)

def handle_car_exited():
    print("Car exited: ")
    port = os.getenv('SERVO_PORT')
    servo = Servo(port)
    servo.connect()
    servo.move_servo(90)
    time.sleep(4)
    servo.move_servo(45)

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
