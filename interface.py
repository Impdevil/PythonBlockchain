import os
from flask import Flask
from io import StringIO

from flask import flash ,request,redirect,url_for
import requests
import time
import Blockchain as bc
import json
from werkzeug.utils import secure_filename
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_text_to_fp


class interface_methods():
    def Announce_New_Block(self, block):
        for Peer in peers:
            url = "https://{}/add_block".format(peer)
            requests.post(url,data=json.dumps(block.__dict__, sort_keys=True))

    def allowed_file(self , filename):
        extention = str(filename.rsplit(".",1)[1].lower())
        print(extention)
        if extention in ALLOWED_EXTENSIONS:
            print("True")
            return True
        print("p1 False")
        return False
     
UPLOAD_FOLDER = "/Uploads/"
ALLOWED_EXTENSIONS = ["pdf"]    
app = Flask(__name__)
interface = interface_methods()
blockchain = bc.Blockchain()
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/Make_Contractblock" , methods=["GET","POST"])
def Create_Block():
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data action="/Add_to_Pending">
      <input type=file name=file>
      <input type=text name=Author>
      <input type=submit value=Upload>
    </form>
    '''

    """

@app.route('/Add_to_Pending', methods=['POST'])
def New_Vote():
    print("Json? >> "+ str(request.is_json))
    if "file" not in request.files:
        flash("no PDF!")
        return redirect(request.url)
    file = request.files["file"]
    print(file.filename)
    #tx_data = request.get_json()
    tx_data = request.get_data(as_text=True)
    print(str(tx_data))
    if file.filename == "":
        flash("No Selected File")
        return redirect(request.url)
    if interface.allowed_file(file.filename) == True:
        print(str(file))
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"]))
        #pdf_html = StringIO()
        #extract_text_to_fp(file,pdf_html,laparams =LAParams(),output_type="html",codec=None )
        #print("pdf: "+ pdf_html.get_value() )
        tx_data["Content"] = filename

    print("Data : "+str(tx_data))
    required_fields = ["Author" , "Content"]
    for field in required_fields:
        if not tx_data.get(field):
            return"invalid Contract Data", 404
    tx_data["timestamp"] = time.time()
    blockchain.Add_New_VoteTrade(tx_data)

    return "Success",201


@app.route('/get_chain', methods=['GET'])
def Get_Chain():
    chain_data=[]
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"lenght":len(chain_data),"chain": chain_data })

@app.route('/mine',methods=['GET'])
def Mine_Unconfirmed_Transactions():
    result = blockchain.mine(interface)
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
        length = response.json()['lenght']
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
    block = PyBlock.Block(block_data['index'], block_data['Contracts'], block_data["timestamp"], block_data["Previous_hash"])
    proof = block_data['hash']
    added = blockchain.add_block(block,proof)
    if not added:
        return "the block was discarded by the node", 400
    return "Block added to the chain", 201
    

app.run(debug=True, port=8000)

