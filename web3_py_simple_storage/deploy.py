from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os

from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# Compile solidity code
compiled_solidity_code = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_solidity_code.json", "w") as file:
    json.dump(compiled_solidity_code, file)

# Get the bytecode (Fetching from compiled_solidity_code.json file)
bytecode = compiled_solidity_code["contracts"]["SimpleStorage.sol"][
    "firstContractSimpleStorage"
]["evm"]["bytecode"]["object"]

# Get the ABI (Fetching from compiled_solidity_code.json file)
abi = compiled_solidity_code["contracts"]["SimpleStorage.sol"][
    "firstContractSimpleStorage"
]["abi"]

# For connecting to Ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/5904c36cf4f0488aa232396e66e40c32")
)
chain_id = 4
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in Python
SimpleStorageContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Create the NONCE & Pre-estimated GasPrice to be used
nonce = w3.eth.getTransactionCount(my_address)
gas_price = w3.eth.gas_price

# To complete the transaction, we will need to -
# 1) Build the transaction
# 2) Sign the transaction
# 3) Send the transaction

transaction = SimpleStorageContract.constructor().buildTransaction(
    {"gasPrice": gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce}
)

# 2) Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# 3) Send the transaction
print("Deploying the contract ...")
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Deployment Successful !")

# To work with contract, we need -
# Contract Address & Contract ABI
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# There are 2 ways to interact with the contract
# 1) Call -> Simulate making the function call & getting return value
# 2) Transact -> Actually making the state change

# Initial value of Age
print(simple_storage.functions.retrieve().call())

print("Updating the contract ...")
# Update the Age by using changeVal function
# print(simple_storage.functions.changeVal(29).call())
store_transaction = simple_storage.functions.changeVal(29).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1, "gasPrice": gas_price}
)

signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key
)

transaction_hash = w3.eth.send_raw_transaction(signed_store_transaction.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print("Contract updated !")
print(simple_storage.functions.retrieve().call())
