import hashlib

class MikeCoinBlock:

    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = "-".join(transaction_list) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

t1 = "Anna sends 2 MC to Mike"
t2 = "Bob sends 0.5 MC to Mike"
t3 = "Mike sends 3.2 MC to Bob"
t4 = "Daniel sends 0.3 MC to Anna"
t5 = "Mike sends 1 MC to Charlie"
t6 = "Mike sends 5.4 MC to Daniel"

initial_block = MikeCoinBlock("Initial String", [t1, t2])

print(initial_block.block_data)
print(initial_block.block_hash)

second_block = MikeCoinBlock(initial_block.block_hash, [t3, t4])

print(second_block.block_data)
print(second_block.block_hash)

third_block = MikeCoinBlock(second_block.block_hash, [t5, t6])

print(third_block.block_data)
print(third_block.block_hash)

###################################################################

m = hashlib.sha256()
m.update(b"The butterfly effect is a criminally underrated")
print(m.hexdigest())

def new_block(self, proof, previous_hash):

    block = {
        'index': len(self.chain) + 1,
        'timestamp': time(),
        'transactions': self.current_transactions,
        'previous_hash': previous_hash or self.hash(self.chain[-1]),
        'proof': proof,
    }

    self.current_transactions = []
    self.chain.append(block)
    return block


def hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()


def proof_of_work(self, last_block):
    last_proof = last_block['proof']
    last_hash = self.hash(last_block)

    proof = 0
    while self.valid_proof(lst_proof, proof, last_hash) is False:
        proof += 1
    return proof

@staticmethod
def valid_proof(last_proof, proof, last_hash):
    guess = f'{last_proof}{proof}{last_hash}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    # the more zeros, the more difficult the work
    return guess_hash[:4] == "0000"


def mine():

    start_time = time()
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)
    elapsed = time() - start_time

    blockchain.new_transaction(
        sender="MikeCoin Mining Reward",
        recipient=node_identifier,
        amount=3,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'nessage': "New Block mined and added to the chain!",
        'index': block['index'],
        'transactions': block['transactions'],
        'previous_hash': block['previous_hash'],
        'the answer was ': block['proof'],
        'seconds required to solve ': elapsed
    }
    return jsonify(response), 200
