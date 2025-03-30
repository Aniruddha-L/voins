from web3 import Web3
from pymongo import MongoClient

url = 'http://127.0.0.1:7545'
web3 = Web3(Web3.HTTPProvider(url))
mongo = MongoClient('mongodb+srv://Aniruddha:Anis301004@users.46fh9to.mongodb.net/')
db = mongo['AI']
ins = db['References']
coll = db['Disease']
if web3.is_connected():
    print('Connected')

else:
    raise Exception('Not connected')

web3.eth.account.create
deployer = web3.eth.accounts[0]

id = 1
lst = ['Arthritis', 'Asthma', 'Cancer', 'Diabetes', 'Hypertension', 'Obesity']
a = ins.find_one({"_id":1}, {"abi":1, "bytecode":1, "_id":0})
abi = a['abi']
byte = a['bytecode']

Insurance = web3.eth.contract(abi=abi, bytecode=byte)
tx_hash = Insurance.constructor().transact({"from": deployer})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
insurance_contract = web3.eth.contract(address=contract_address, abi=abi)

for i in lst:
    print(contract_address)
    tx = insurance_contract.functions.setDisease(i).transact({'from':deployer})
    recipt = web3.eth.wait_for_transaction_receipt(tx)
    print('hex',recipt.transactionHash.hex())
    print('block: ', recipt.blockNumber)
    print(insurance_contract.functions.getDisease().call())

    data = {
        "_id":id,
        'name':i,
        'add':contract_address,
        'block':recipt.blockNumber
    }
    id += 1
    coll.insert_one(data)