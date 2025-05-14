import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("HOLESKY_RPC")))
assert w3.is_connected(), "❌ Failed to connect to Holesky"

my_address = os.getenv("WALLET_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")

with open("blockchain/contract_abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)

vector = [0.12, 0.22, 0.33]
embedding_bytes = json.dumps(vector).encode("utf-8")
embedding_hash = Web3.keccak(embedding_bytes)

nonce = w3.eth.get_transaction_count(my_address)
gas_price = w3.to_wei("8", "gwei")  

tx = contract.functions.storeVector("constitution.pdf", embedding_hash).build_transaction({
    'from': my_address,
    'nonce': nonce,
    'gas': 200000,
    'gasPrice': gas_price,
    'chainId': 17000
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("✅ Vector stored on-chain!")
print("🔗 Holesky Etherscan:", f"https://holesky.etherscan.io/tx/{tx_hash.hex()}")
print("RPC:", os.getenv("HOLESKY_RPC"))
print("Nonce:", nonce)
print("Gas price (gwei):", w3.from_wei(gas_price, "gwei"))
print("Embedding hash:", embedding_hash.hex())
receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
print("✅ Confirmed in block:", receipt.blockNumber)
