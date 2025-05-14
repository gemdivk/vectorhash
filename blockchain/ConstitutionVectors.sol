// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ConstitutionVectors {
    struct VectorRef {
        uint id;
        string docTitle;
        bytes32 embeddingHash;
    }

    mapping(uint => VectorRef) public vectors;
    uint public vectorCount;

    function storeVector(string memory docTitle, bytes32 embeddingHash) public {
        vectorCount++;
        vectors[vectorCount] = VectorRef(vectorCount, docTitle, embeddingHash);
    }

    function getVector(uint id) public view returns (string memory, bytes32) {
        return (vectors[id].docTitle, vectors[id].embeddingHash);
    }
}
