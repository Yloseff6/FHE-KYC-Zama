from concrete import fhe
from web3 import Web3
import json

@fhe.compiler({"kyc_passed": "bool"})
def encrypt_kyc(kyc_passed: bool):
    return kyc_passed

def main():
    circuit = encrypt_kyc.compile()
    encrypted = circuit.encrypt(kyc_passed=True)
    proof = encrypted.serialize()

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    if not w3.is_connected():
        print("❌ Cannot connect to FHEVM node.")
        return

    account = w3.eth.accounts[0]

    with open("contracts/PrivateKYC.abi.json") as f:
        abi = json.load(f)

    contract_address = "0xYourContractAddressHere"  # Заменить на реальный адрес
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(contract_address),
        abi=abi
    )

    try:
        tx_hash = contract.functions.submitProof(proof).transact({'from': account})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f"✅ Proof sent successfully. TX Hash: {tx_hash.hex()}")
        else:
            print(f"❌ Transaction failed. TX Hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"❌ Error sending proof: {e}")

if __name__ == "__main__":
    main()
