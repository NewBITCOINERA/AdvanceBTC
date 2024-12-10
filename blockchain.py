import hashlib
import time
import json
import random

# Block class to define the structure of each block
class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, merkle_root, hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.hash = hash

    def calculate_merkle_root(self):
        """Calculate the Merkle Root for the block's transactions."""
        transactions_hashes = [hashlib.sha256(tx.encode('utf-8')).hexdigest() for tx in self.transactions]
        while len(transactions_hashes) > 1:
            if len(transactions_hashes) % 2 != 0:
                transactions_hashes.append(transactions_hashes[-1])
            transactions_hashes = [hashlib.sha256((transactions_hashes[i] + transactions_hashes[i+1]).encode('utf-8')).hexdigest() for i in range(0, len(transactions_hashes), 2)]
        return transactions_hashes[0]  # The Merkle Root

# Function to calculate the hash of a block
def calculate_block_hash(index, previous_hash, timestamp, merkle_root):
    """Calculate the block hash with Merkle Root."""
    block_string = f"{index}{previous_hash}{timestamp}{merkle_root}"
    return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

# Blockchain class to handle the blockchain operations
class Blockchain:
    def __init__(self, validators=None):
        self.chain = []
        self.current_transactions = []
        self.proof_of_stake = ProofOfStake(validators) if validators else None
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the chain (genesis block)."""
        genesis_block = Block(0, time.time(), [], "0", "0", "0")
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        """Add a block to the blockchain."""
        index = len(self.chain)
        previous_hash = self.chain[-1].hash
        timestamp = time.time()
        merkle_root = Block(index, timestamp, transactions, previous_hash, "", "").calculate_merkle_root()
        hash = calculate_block_hash(index, previous_hash, timestamp, merkle_root)
        new_block = Block(index, timestamp, transactions, previous_hash, merkle_root, hash)
        self.chain.append(new_block)

        return new_block

    def print_chain(self):
        """Print the blockchain."""
        for block in self.chain:
            print(f"Block #{block.index} [Hash: {block.hash}]")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.transactions}\n")

    def is_chain_valid(self):
        """Check if the blockchain is valid by verifying each block."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's previous hash matches the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                return False

            # Check if the current block's hash is correct
            if current_block.hash != calculate_block_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.merkle_root):
                return False

        return True

# Proof of Stake (PoS) class for block validation
class ProofOfStake:
    def __init__(self, validators):
        self.validators = validators

    def select_validator(self):
        """Select a validator based on their stake."""
        total_stake = sum([validator['stake'] for validator in self.validators])
        selection = random.randint(1, total_stake)
        running_total = 0
        for validator in self.validators:
            running_total += validator['stake']
            if running_total >= selection:
                return validator
        return self.validators[-1]

# Example of using the blockchain and PoS classes
if __name__ == "__main__":
    # Define validators with their stake amounts (for Proof of Stake)
    validators = [
        {"name": "Alice", "stake": 100},
        {"name": "Bob", "stake": 200},
        {"name": "Charlie", "stake": 300}
    ]

    # Initialize the blockchain with validators
    blockchain = Blockchain(validators)

    # Add some blocks
    blockchain.add_block([{"sender": "Alice", "receiver": "Bob", "amount": 50}])
    blockchain.add_block([{"sender": "Bob", "receiver": "Charlie", "amount": 30}])

    # Print the blockchain
    blockchain.print_chain()

    # Verify the blockchain integrity
    print("Blockchain valid:", blockchain.is_chain_valid())
