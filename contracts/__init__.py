from .wallet import Wallet
from web3 import Web3
from solcx import compile_source

wallet = Wallet()

def parking_lot_contract(w3: Web3, contractAddress: str):
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
    parking_lot = w3.eth.contract(
        address=contractAddress,
        abi=abi
    )
    return parking_lot
