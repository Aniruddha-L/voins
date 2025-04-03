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
    
    def getAllIns(self):
        a = self.ref.find_one({"_id": 3}, {"abi": 1, "_id": 0})
        abi = a['abi']
        self.ins = self.db['Insurance']
        data = self.ins.find({}, {"_id":0, "name":0})
        a = []
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
                        
                        a.append(function_args['ins'])
                    except Exception as e:
                        print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
        return a

    def getAllDisease(self):
        a = self.ref.find_one({"_id": 1}, {"abi": 1, "_id": 0})
        abi = a['abi']
        self.ins = self.db['Disease']
        data = self.ins.find({}, {"_id":0, "name":0})
        a = []
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
                        
                        a.append(function_args['dis'])
                        # print(decoded_input)
                    except Exception as e:
                        print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
        return a
    
    def getAllHospital(self):
        a = self.ref.find_one({"_id": 2}, {"abi": 1, "_id": 0})
        abi = a['abi']
        self.ins = self.db['Hospital']
        data = self.ins.find({}, {"_id":0, "name":0})
        a =[]
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
                        
                        a.append(function_args['hospital'])
                    except Exception as e:
                        print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
            return a
    
    def getAIns(self, insName):
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
                        if function_args['ins'] == insName:
                            print(function_args)
                            return (block, address)
                    except Exception as e:
                        print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
            else:
               return self.setIns(insName)
    
    def getADisease(self, disName):
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
                        
                        if (function_args['dis'] == disName):
                            return (block, address)
                        # print(decoded_input)
                    except Exception as e:
                        print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
            else:
                return self.setDisease(disName)
    def getAHospital(self, disName):
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
                        
                        if (function_args['hospital'] == disName):
                            return (block, address)
                        # print(decoded_input)
                    except Exception as e:
                        print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
            else:
                return self.setHos(disName)
    def getDisease(self, add, blk):
        a = self.ref.find_one({"_id": 1}, {"abi": 1, "_id": 0})
        abi = a['abi']
        address = add
        block = blk
        contract = self.web3.eth.contract(address=address, abi=abi)
        contract_block = self.web3.eth.get_block(block, full_transactions=True)
        for tx in contract_block.transactions:
            if tx.input and tx.input != "0x":  # Ensure there is input data
                try:
                    # Decode function call using ABI
                    decoded_input = contract.decode_function_input(tx.input)
                    function_name, function_args = decoded_input
                    
                    return function_args['dis']
                except Exception as e:
                    print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
    def getHospital(self, addr, blk):
        a = self.ref.find_one({"_id": 2}, {"abi": 1, "_id": 0})
        abi = a['abi']
        address = addr
        block = blk
        contract = self.web3.eth.contract(address=address, abi=abi)
        contract_block = self.web3.eth.get_block(block, full_transactions=True)
        for tx in contract_block.transactions:
            if tx.input and tx.input != "0x":  # Ensure there is input data
                try:
                    # Decode function call using ABI
                    decoded_input = contract.decode_function_input(tx.input)
                    function_name, function_args = decoded_input
                    
                    return function_args['hospital']
                except Exception as e:
                    print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")

    def getInsurance(self, add, blk):
        a = self.ref.find_one({"_id": 3}, {"abi": 1, "_id": 0})
        abi = a['abi']
        block = blk
        contract = self.web3.eth.contract(address=add, abi=abi)
        contract_block = self.web3.eth.get_block(block, full_transactions=True)
        for tx in contract_block.transactions:
            if tx.input and tx.input != "0x":  # Ensure there is input data
                try:
                    # Decode function call using ABI
                    decoded_input = contract.decode_function_input(tx.input)
                    function_name, function_args = decoded_input
                    
                    return function_args['ins']
                except Exception as e:
                    print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")

    def setUser(self, user, hBlk, IBlk):
        coll = self.db['Users']
        a = self.ref.find_one({"_id": 5}, {"abi": 1,"bytecode":1, "_id": 0})
        abi = a['abi']
        # print(a)
        byte = a['bytecode']
        Insurance = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_hash = Insurance.constructor().transact({'from': self.web3.eth.default_account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        insurance_contract = self.web3.eth.contract(address=contract_address, abi=abi)
        tx = insurance_contract.functions.setUser(user, hBlk, IBlk).transact({'from': self.web3.eth.default_account})
        recipt = self.web3.eth.wait_for_transaction_receipt(tx)
        last = coll.find({}, {"_id":1}).sort("_id", -1).limit(1)
        try:
            last = last.next()["_id"]
        except StopIteration:
            last = 0
        data = {
                "_id":last+1,
                'name':user,
                'hospital':hBlk,
                'Insurance':IBlk
        }
        coll.insert_one(data)
        return (contract_address, recipt.blockNumber)
    
    def setDisease(self,Dis):
        coll = self.db['Disease']
        a = self.ref.find_one({"_id": 1}, {"abi": 1,"bytecode":1, "_id": 0})
        abi = a['abi']
        # print(a)
        byte = a['bytecode']
        Insurance = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_hash = Insurance.constructor().transact({'from': self.web3.eth.default_account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        insurance_contract = self.web3.eth.contract(address=contract_address, abi=abi)
        tx = insurance_contract.functions.setDisease(Dis).transact({'from': self.web3.eth.default_account})
        recipt = self.web3.eth.wait_for_transaction_receipt(tx)
        last = coll.find({}, {"_id":1}).sort("_id", -1).limit(1)
        try:
            last = last.next()["_id"]+1
        except StopIteration:
            last = 0
        data = {
            "_id":last,
            "disease":Dis,
            "add":contract_address,
            "blk":recipt.blockNumber
        }
        coll.insert_one(data)
        return (contract_address, recipt.blockNumber)
    def setIns(self,Dis):
        coll = self.db['Disease']
        a = self.ref.find_one({"_id": 3}, {"abi": 1,"bytecode":1, "_id": 0})
        abi = a['abi']
        # print(a)
        byte = a['bytecode']
        Insurance = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_hash = Insurance.constructor().transact({'from': self.web3.eth.default_account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        insurance_contract = self.web3.eth.contract(address=contract_address, abi=abi)
        tx = insurance_contract.functions.setIns(Dis).transact({'from': self.web3.eth.default_account})
        recipt = self.web3.eth.wait_for_transaction_receipt(tx)
        last = coll.find({}, {"_id":1}).sort("_id", -1).limit(1)
        try:
            last = last.next()["_id"]
        except StopIteration:
            last = 0
        return (contract_address, recipt.blockNumber)
    def setHos(self,Dis):
        coll = self.db['Disease']
        a = self.ref.find_one({"_id": 2}, {"abi": 1,"bytecode":1, "_id": 0})
        abi = a['abi']
        # print(a)
        byte = a['bytecode']
        Insurance = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_hash = Insurance.constructor().transact({'from': self.web3.eth.default_account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        insurance_contract = self.web3.eth.contract(address=contract_address, abi=abi)
        tx = insurance_contract.functions.setHospital(Dis).transact({'from': self.web3.eth.default_account})
        recipt = self.web3.eth.wait_for_transaction_receipt(tx)
        last = coll.find({}, {"_id":1}).sort("_id", -1).limit(1)
        try:
            last = last.next()["_id"]
        except StopIteration:
            last = 0
        return (contract_address, recipt.blockNumber)
    
    def getUser(self, add, block):
        a = self.ref.find_one({"_id": 5}, {"abi": 1,"bytecode":1, "_id": 0})
        abi = a['abi']
        # print(a)
        byte = a['bytecode']
        Insurance = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_hash = Insurance.constructor().transact({'from': self.web3.eth.default_account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        insurance_contract = self.web3.eth.contract(address=add, abi=abi)
        contract_block = self.web3.eth.get_block(block, full_transactions=True)
        for tx in contract_block.transactions:
            if tx.input and tx.input != "0x":  # Ensure there is input data
                try:
                    # Decode function call using ABI
                    decoded_input = insurance_contract.decode_function_input(tx.input)
                    function_name, function_args = decoded_input
                    
                    return function_args['User']
                except Exception as e:
                    print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
    
    # def getHospital(self, disName):
    #     a = self.ref.find_one({"_id": 5}, {"abi": 1, "_id": 0})
    #     abi = a['abi']
    #     self.ins = self.db['Hospital']
    #     data = self.ins.find({}, {"_id":0, "name":0})
    #     for i in data:
    #         address = i['add']
    #         block = i['block']
    #         contract = self.web3.eth.contract(address=address, abi=abi)
    #         contract_block = self.web3.eth.get_block(block, full_transactions=True)
    #         for tx in contract_block.transactions:
    #             if tx.input and tx.input != "0x":  # Ensure there is input data
    #                 try:
    #                     # Decode function call using ABI
    #                     decoded_input = contract.decode_function_input(tx.input)
    #                     function_name, function_args = decoded_input
                        
    #                     if (function_args['User'] == disName):
    #                         return (block, address)
    #                     # print(decoded_input)
    #                 except Exception as e:
    #                     print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
    #         else:
    #             return self.setUser(disName)

    def getTerms(self, add, blk):
        a = self.ref.find_one({"_id":4}, {"abi":1, "bytecode":1, "_id":0})
        abi = a['abi']
        # print(a)
        byte = a['bytecode']
        contract = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_has = contract.constructor().transact({"from":self.web3.eth.default_account})
        txR = self.web3.eth.wait_for_transaction_receipt(tx_has)
        insurance_contract = self.web3.eth.contract(address=add, abi=abi)
        contract_block = self.web3.eth.get_block(blk, full_transactions=True)
        for tx in contract_block.transactions:
            if tx.input and tx.input != "0x":  # Ensure there is input data
                try:
                    # Decode function call using ABI
                    decoded_input = insurance_contract.decode_function_input(tx.input)
                    # print(decoded_input)
                    function_name, function_args = decoded_input
                    
                    return function_args['rules']
                except Exception as e:
                    print(f"Transaction {tx.hash.hex()} contains non-decodable data: {e}")
    
    def setTerms(self, data, ins):
        coll = self.db['Terms']
        a = self.ref.find_one({"_id": 4}, {"abi": 1,"bytecode":1, "_id": 0})
        abi = a['abi']
        # print(a)
        byte = a['bytecode']
        Insurance = self.web3.eth.contract(abi=abi, bytecode=byte)
        tx_hash = Insurance.constructor().transact({'from': self.web3.eth.default_account})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        insurance_contract = self.web3.eth.contract(address=contract_address, abi=abi)
        tx = insurance_contract.functions.setTerms(data, ins).transact({'from': self.web3.eth.default_account})
        recipt = self.web3.eth.wait_for_transaction_receipt(tx)
        last = coll.find({}, {"_id":1}).sort("_id", -1).limit(1)
        try:
            last = last.next()["_id"]
        except StopIteration:
            last = 0
        data = {
            "_id":last,
            "ins":ins,
            "data":data,
            "add":contract_address,
            "blk":recipt.blockNumber
        }
        return (contract_address, recipt.blockNumber)
        
if __name__=='__main__':
    a = Access()
    add, blk = a.setTerms('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 1)
    print(a.getTerms(add, blk))