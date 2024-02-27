from contracts.wallet import Wallet
from contracts import parking_lot_contract
from web3 import Web3

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
