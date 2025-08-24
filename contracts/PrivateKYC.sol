// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PrivateKYC {
    mapping(address => bytes) private proofs;

    event ProofSubmitted(address indexed user);

    function submitProof(bytes calldata encryptedProof) external {
        require(encryptedProof.length > 0, "Proof cannot be empty");
        proofs[msg.sender] = encryptedProof;
        emit ProofSubmitted(msg.sender);
    }

    function hasProof(address user) external view returns (bool) {
        return proofs[user].length > 0;
    }

    function getProof(address user) external view returns (bytes memory) {
        return proofs[user];
    }
}
