from concrete import fhe
from web3 import Web3
import json

# Компилируем FHE-шифратор
@fhe.compiler({"kyc_passed": "bool"})
def encrypt_kyc(kyc_passed: bool):
    return kyc_passed

circuit = encrypt_kyc.compile()
encrypted = circuit.encrypt(kyc_passed=True)
proof = encrypted.serialize()

# Подключение к локальному FHEVM
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
account = w3.eth.accounts[0]

# Загрузка ABI
with open("contracts/PrivateKYC.abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address("0xYourContractAddressHere"),
    abi=abi
)

tx = contract.functions.submitProof(proof).transact({'from': account})
print(f"✅ Proof sent. TX Hash: {tx.hex()}")
