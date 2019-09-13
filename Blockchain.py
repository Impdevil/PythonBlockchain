import time
import Block as PyBlock
import Interface

class Blockchain():
    difficulty =4
    def __init__(self):
        self.unconfirmed_votes = [] ## data yet to be sent to a block
        self.chain = []
        self.Create_Genesis_Block()
    def Create_Genesis_Block(self):
        """creates the first Block for the chain to start the chain
            Block index = 0 && previous_hash = 0 && output hash is correct
        """
        genesisBlock = PyBlock.Block(0,[],time.time(),"0")
        genesisBlock.hash = genesisBlock.Compute_Hash()
        self.chain.append(genesisBlock)
        print("hash: "+ genesisBlock.hash)

    @property
    def Last_Block(self):
        print("chain last block: "+str(self.chain[len(self.chain)-1].timestamp))

        return self.chain[-1]

    def Proof_Of_Work(self,block):
        """brute force a new hash with the right difficulty rating"""
        block.nonce=0
        computedHash = block.Compute_Hash()
        while not computedHash.startswith('0' * Blockchain.difficulty):
            block.nonce+=1
            computedHash = block.Compute_Hash()
        return computedHash

    def Add_Block(self, block, proof):
        """ adds a new block to the chain but varifies it with the chain first"""
        previous_hash = self.Last_Block.hash
        if previous_hash != block.Previous_Hash:
            return False
        if not self.Is_Valid_Proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def Is_Valid_Proof(self,block,block_hash):
        """Makes sure the the hash is correct for the chain aswell as the contents of the block are 
        correctly hashed
        """       
        return(block_hash.startswith("0"*Blockchain.difficulty) and block_hash == block.Compute_Hash())

    def Add_New_VoteTrade(self, vote):
        self.unconfirmed_votes.append(vote)

    def mine(self):
        """Builds the interface for build the blockchain and distributing id"""
        if not self.unconfirmed_votes:
            return False

        lastBlock = self.chain[len(self.chain) -1]
        new_block = PyBlock.Block(index=lastBlock.index+1,
                            vote_data = self.unconfirmed_votes,
                            timestamp = time.time(),
                            PREV_hash = lastBlock.hash)
        proof = self.Proof_Of_Work(new_block)
        self.Add_Block(new_block, proof)
        self.unconfirmed_votes =[]
        Interface.Announce_New_Block(new_block)
        return new_block.index
    #
