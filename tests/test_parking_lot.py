from web3 import Web3
from web3.exceptions import ContractLogicError
from solcx import compile_source
import json
import pytest
from contracts import parking_lot_contract

from client import enter as car_enter

def test_enter_and_exit_parking_lot():

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

    # Connect to Hardhat node
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    # Set up your account
    w3.eth.default_account = w3.eth.accounts[0]  # Use one of the Ganache accounts or your testnet account

    # Deploy the contract
    ParkingLot = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = ParkingLot.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    address = tx_receipt.contractAddress

    parking_lot = parking_lot_contract(w3, address)

    # Interact with the contract
    #enter_tx = parking_lot.functions.enter().transact({'value': w3.to_wei(0.00001, 'ether')})
    #w3.eth.wait_for_transaction_receipt(enter_tx)
    #exit_tx = parking_lot.functions.exit().transact()
    #w3.eth.wait_for_transaction_receipt(exit_tx)

    # Query contract state
    #owner = parking_lot.functions.owner().call()
    #print(f'Contract owner: {owner}')

def test_exit_without_registered():
    # Assuming `contract` is your deployed contract instance
    # and `account` is the account making the transaction.

    insufficient_amount = 0  # Set this to a value known to be insufficient

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

    # Connect to Hardhat node
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    # Set up your account
    w3.eth.default_account = w3.eth.accounts[0]  # Use one of the Ganache accounts or your testnet account

    # Deploy the contract
    ParkingLot = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = ParkingLot.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    parking_lot = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=abi
    )


    with pytest.raises(ContractLogicError) as excinfo:
        exit_tx = parking_lot.functions.exit().transact()
        w3.eth.wait_for_transaction_receipt(exit_tx)

    # Check that the error message contains 'Insufficient payment'
    assert "Car not registered" in str(excinfo.value)

def test_insufficient_payment():
    # Assuming `contract` is your deployed contract instance
    # and `account` is the account making the transaction.

    insufficient_amount = 0  # Set this to a value known to be insufficient

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

    # Connect to Hardhat node
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    # Set up your account
    w3.eth.default_account = w3.eth.accounts[0]  # Use one of the Ganache accounts or your testnet account

    # Deploy the contract
    ParkingLot = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = ParkingLot.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    parking_lot = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=abi
    )

    address = tx_receipt.contractAddress

    with pytest.raises(ContractLogicError) as excinfo:
        car_enter(address, 0.00001)

    assert "Insufficient payment" in str(excinfo.value)
