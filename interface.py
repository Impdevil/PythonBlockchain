from flask import Flask
from flask import request
import requests
import time
import Blockchain as bc
import json

    
class interface_methods():
    def Announce_New_Block(self, block):
        for Peer in peers:
            url = "https://{}/add_block".format(peer)
            requests.post(url,data=json.dumps(block.__dict__, sort_keys=True))


    
app = Flask(__name__)
interface = interface_methods()
blockchain = bc.Blockchain(interface)


@app.route('/new_vote', methods=['POST'])
def New_Vote():
    print("Json? >> "+ str(request.is_json))
    tx_data = request.get_json()
    print("Data : "+str(tx_data))
    required_fields = ["Author" , "Content"]
    for field in required_fields:
        if not tx_data.get(field):
            return"invalid Vote Data", 404
    tx_data["timestamp"] = time.time()
    blockchain.Add_New_VoteTrade(tx_data)

    return "Success",201


@app.route('/', methods=['GET'])
def Get_Chain():
    chain_data=[]
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"lenght":len(chain_data),"chain": chain_data })

@app.route('/mine',methods=['GET'])
def Mine_Unconfirmed_Transactions():
    result = blockchain.mine()
    if not result:
        return "No Votes to Mine"
    return "block #{} is mined.".format(result)

@app.route('/pending_contracts')
def Get_Pending_Votes():
    return json.dumps(blockchain.unconfirmed_Contract)



peers = set()
#endpoint to add new peers to the network.
@app.route('/add_node')
def Register_New_Peer():
    nodes = request.get_json()
    if not nodes:
        return "invalid data", 400
    for node in nodes:
        peers.add(node)
    return "Success" , 201

print("Blockchain lenght: " + str(len(blockchain.chain)))
def Consensus():
    """Simple consensus algorithm, finds the longest Chain and replaces the local one with the larger one
        Local = LongerDistrebuted
    """
    global blockchain
    longest_chain = None
    current_len = len(blockchain.chain)
    for node in peers:
        response = requests.get('http://{}/chain'.format(node))
        length = responce.json()['lenght']
        chain = response.json()['chain']
        if length > current_len and blockchain.Check_Chain_Validity(chain):
            current_len = length
            longest_chain = chain
    if longest_chain:
            blockchain = longest_chain
            return True
    return False

@app.route('/add_block', methods=['POST'])
def Add_and_Validate_Block():
    block_data = request.get_json()
    block = PyBlock.Block(block_data['index'], block_data['transactions'], block_data["timestamp"], block_data["Previous_hash"])
    proof = block_data['hash']
    added = blockchain.add_block(block,proof)
    if not added:
        return "the block was discarded by the node", 400
    return "Block added to the chain", 201
    
class interface_methods():
    def Announce_New_Block(self, block):
        for Peer in peers:
            url = "https://{}/add_block".format(peer)
            requests.post(url,data=json.dumps(block.__dict__, sort_keys=True))


    

app.run(debug=True, port=8000)

