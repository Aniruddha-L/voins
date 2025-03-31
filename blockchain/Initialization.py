from pymongo import MongoClient
from web3 import Web3
import json

class Initialization:
    def __init__(self):
        self.mongoUrl = 'mongodb://localhost:27017/'
        self.GanachUrl = 'http://localhost:7545'
        self.mongo = MongoClient(self.mongoUrl)
        self.web3 = Web3(Web3.HTTPProvider(self.GanachUrl))
        self.db = self.mongo['AI']
        self.ref = self.db['References']
        self.web3.eth.default_account = self.web3.eth.accounts[0]
        self.References()
        self.Insurance()
        self.Disease()
        self.Hospital()

    def Disease(self):
        coll = self.db['Disease']
        id = 1
        lst = ['Arthritis', 'Asthma', 'Cancer', 'Diabetes', 'Hypertension', 'Obesity']
        a = self.ref.find_one({"_id":1}, {"abi":1, "bytecode":1, "_id":0})
        abi = a['abi']
        byte = a['bytecode']
        Insurance = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_hash = Insurance.constructor().transact({'from': self.web3.eth.default_account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        insurance_contract = self.web3.eth.contract(address=contract_address, abi=abi)

        for i in lst:
            print(contract_address)
            tx = insurance_contract.functions.setDisease(i).transact({'from': self.web3.eth.default_account})
            recipt = self.web3.eth.wait_for_transaction_receipt(tx)

            data = {
                "_id":id,
                'name':i,
                'add':contract_address,
                'block':recipt.blockNumber
            }
            id += 1
            try:
                if coll.find_one({'name':i}) is None :
                    coll.insert_one(data)
                else:
                    coll.update_one({'name':i}, {"$set":{"add":contract_address}})
            except Exception:
                print(Exception        )
        
    def Insurance(self):
        coll = self.db['Insurance']
        id = 1
        lst = ['Aetna', 'Blue Cross', 'Cigna', 'Medicare', 'UnitedHealthcare']
        a = self.ref.find_one({"_id":3}, {"abi":1, "bytecode":1, "_id":0})
        abi = a['abi']
        byte = a['bytecode']
        Insurance = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_hash = Insurance.constructor().transact({'from': self.web3.eth.default_account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        insurance_contract = self.web3.eth.contract(address=contract_address, abi=abi)

        for i in lst:
            print(contract_address)
            tx = insurance_contract.functions.setIns(i).transact({'from': self.web3.eth.default_account})
            recipt = self.web3.eth.wait_for_transaction_receipt(tx)

            data = {
                "_id":id,
                'name':i,
                'add':contract_address,
                'block':recipt.blockNumber
            }
            id += 1
            try:
                if coll.find_one({'name':i}) is None:
                    coll.insert_one(data)
                else:
                    coll.update_one({'name':i}, {"$set":{"add":contract_address}})
            except Exception as e:
                print(e)

    def References(self):
        lst = ['Disease', 'Hospitals', 'Insurance', 'Terms', 'Users']
        id = 1
        for i in lst:
            with open(f'build/contracts/{i}.json', 'r') as file:
                data = json.load(file)
                abi = data['abi']
                byte = data['bytecode']
            try:
                data = {
                    "_id":id, 
                    "name":i,
                    "abi":abi,
                    "bytecode":byte
                }
                self.ref.insert_one(data)
            except Exception:
                return print(Exception)
            id += 1

    def Hospital(self):
        coll = self.db['Hospital']
        id = 1
        lst = ['LLC Smith','Ltd Smith','Johnson PLC','Smith Ltd','Smith PLC','Smith Group','Johnson Inc','Smith Inc','Group Smith','Smith LLC']
        a = self.ref.find_one({"_id":2}, {"abi":1, "bytecode":1, "_id":0})
        abi = a['abi']
        byte = a['bytecode']
        Insurance = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_hash = Insurance.constructor().transact({'from': self.web3.eth.default_account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        insurance_contract = self.web3.eth.contract(address=contract_address, abi=abi)

        for i in lst:
            print(contract_address)
            tx = insurance_contract.functions.setHospital(i).transact({'from': self.web3.eth.default_account})
            recipt = self.web3.eth.wait_for_transaction_receipt(tx)

            data = {
                "_id":id,
                'name':i,
                'add':contract_address,
                'block':recipt.blockNumber
            }
            id += 1
            try:
                if coll.find_one({'name':i}) is None:
                    coll.insert_one(data)
                else:
                    coll.update_one({'name':i}, {"$set":{"add":contract_address}})
            except Exception:
                return None
i = Initialization()
i.Insurance()
# i.Disease()
# i.Hospital()