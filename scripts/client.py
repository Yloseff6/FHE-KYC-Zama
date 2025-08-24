from concrete import fhe
from web3 import Web3
import json

@fhe.compiler({"kyc_passed": "bool"})
def encrypt_kyc(kyc_passed: bool):
    return kyc_passed

def main():
    # Connect to FHEVM node
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    if not w3.is_connected():
        print("❌ Cannot connect to FHEVM node.")
        return

    # Get account
    try:
        account = w3.eth.accounts[0]
    except Exception as e:
        print(f"❌ Unable to get accounts: {e}")
        return

    # Load contract ABI
    try:
        with open("contracts/PrivateKYC.abi.json") as f:
            abi = json.load(f)
    except Exception as e:
        print(f"❌ Error loading contract ABI: {e}")
        return

    # Contract address (replace with your deployed contract address)
    contract_address = "0xYourContractAddressHere"

    # Create contract instance
    try:
        contract = w3.eth.contract(address=contract_address, abi=abi)
    except Exception as e:
        print(f"❌ Error creating contract instance: {e}")
        return

    # Generate encrypted proof
    circuit = encrypt_kyc.compile()
    encrypted = circuit.encrypt(kyc_passed=True)
    proof = encrypted.serialize()

    # Send proof to contract
    try:
        tx_hash = contract.functions.submitProof(proof).transact({'from': account})
        print(f"⏳ Transaction sent. TX Hash: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f"✅ Proof submitted successfully! TX Hash: {tx_hash.hex()}")
        else:
            print(f"❌ Transaction failed. TX Hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"❌ Error sending proof: {e}")

if __name__ == "__main__":
    main()
