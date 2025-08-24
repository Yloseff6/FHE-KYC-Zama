from concrete import fhe

@fhe.compiler({"kyc_passed": "bool"})
def encrypt_kyc(kyc_passed: bool):
    return kyc_passed
