from web3 import Web3
from pymongo import MongoClient

class Access:
    def __init__(self):
        self.mongoUrl = 'mongodb://localhost:27017/'
        self.GanachUrl = 'http://localhost:7545'
        self.mongo = MongoClient(self.mongoUrl)
        self.web3 = Web3(Web3.HTTPProvider(self.GanachUrl))
        self.db = self.mongo['AI']
        self.ref = self.db['References']
        self.web3.eth.default_account = self.web3.eth.accounts[0]
    
    def getIns(self):
        a = self.ref.find_one({"_id": 3}, {"abi": 1, "_id": 0})
        abi = a['abi']
        self.ins = self.db['Insurance']
        data = self.ins.find({}, {"_id":0, "name":0})
        for i in data:
            address = i['add']
            block = i['block']
            contract = self.web3.eth.contract(address=address, abi=abi)
            contract_block = self.web3.eth.get_block(block, full_transactions=True)
            for tx in contract_block.transactions:
                if tx.input and tx.input != "0x":  # Ensure there is input data
                    try:
                        # Decode function call using ABI
                        decoded_input = contract.decode_function_input(tx.input)
                        function_name, function_args = decoded_input
                        print(function_args['ins'])
                    except Exception as e:
                        print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")

    def getDisease(self):
        a = self.ref.find_one({"_id": 1}, {"abi": 1, "_id": 0})
        abi = a['abi']
        self.ins = self.db['Disease']
        data = self.ins.find({}, {"_id":0, "name":0})
        for i in data:
            address = i['add']
            block = i['block']
            contract = self.web3.eth.contract(address=address, abi=abi)
            contract_block = self.web3.eth.get_block(block, full_transactions=True)
            for tx in contract_block.transactions:
                if tx.input and tx.input != "0x":  # Ensure there is input data
                    try:
                        # Decode function call using ABI
                        decoded_input = contract.decode_function_input(tx.input)
                        function_name, function_args = decoded_input
                        print(function_args['dis'])
                        # print(decoded_input)
                    except Exception as e:
                        print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")

    def getHospital(self):
        a = self.ref.find_one({"_id": 2}, {"abi": 1, "_id": 0})
        abi = a['abi']
        self.ins = self.db['Hospital']
        data = self.ins.find({}, {"_id":0, "name":0})
        for i in data:
            address = i['add']
            block = i['block']
            contract = self.web3.eth.contract(address=address, abi=abi)
            contract_block = self.web3.eth.get_block(block, full_transactions=True)
            for tx in contract_block.transactions:
                if tx.input and tx.input != "0x":  # Ensure there is input data
                    try:
                        # Decode function call using ABI
                        decoded_input = contract.decode_function_input(tx.input)
                        function_name, function_args = decoded_input
                        print(function_args['hospital'])
                    except Exception as e:
                        print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")

a = Access()
a.getDisease()