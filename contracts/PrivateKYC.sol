// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PrivateKYC {
    mapping(address => bytes) private proofs;

    function submitProof(bytes calldata encryptedProof) external {
        proofs[msg.sender] = encryptedProof;
    }

    function hasProof(address user) external view returns (bool) {
        return proofs[user].length > 0;
    }

    function getProof(address user) external view returns (bytes memory) {
        return proofs[user];
    }
}
