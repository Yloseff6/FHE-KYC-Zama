import unittest
from concrete import fhe

@fhe.compiler({"kyc_passed": "bool"})
def encrypt_kyc(kyc_passed: bool):
    return kyc_passed

class TestFHEKYC(unittest.TestCase):
    def test_encryption(self):
        circuit = encrypt_kyc.compile()
        encrypted = circuit.encrypt(kyc_passed=True)
        serialized = encrypted.serialize()
        self.assertIsInstance(serialized, bytes)

if __name__ == "__main__":
    unittest.main()
