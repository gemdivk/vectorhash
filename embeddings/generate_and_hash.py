import json
from web3 import Web3

def hash_vector(vector):
    as_bytes = json.dumps(vector).encode("utf-8")
    return Web3.keccak(as_bytes)

# Example usage:
# vector = [0.12, -0.31, 0.88]
# print(hash_vector(vector))