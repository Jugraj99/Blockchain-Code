import json
import hashlib
import time
import os

class Blockchain:
    def __init__(self):
        self.chain = []
        self.validators = {"validator1", "validator2", "validator3"}  # List of authorized validators
        self.load_chain()

    def create_block(self, imei, status, region, operator, validator):
        if validator not in self.validators:
            print(f"❌ Unauthorized validator: {validator}")
            return None  # Unauthorized validator

        previous_hash = self.get_last_block_hash()
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "devices": {imei: status},
            "region": region,
            "operator": operator,
            "validator": validator,
            "previous_hash": previous_hash
        }
        block["hash"] = self.calculate_hash(block)
        return block

    def calculate_hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_device(self, imei, status, region, operator, validator):
        if self.device_exists(imei):
            print(f"IMEI {imei} already exists in the blockchain.")
            return False

        new_block = self.create_block(imei, status, region, operator, validator)
        if not new_block:
            return False  # Block creation failed due to unauthorized validator

        self.chain.append(new_block)
        self.save_chain()
        print(f"✅ IMEI {imei} added successfully!")
        return True

    def device_exists(self, imei):
        return any(imei in block["devices"] for block in self.chain)

    def get_last_block_hash(self):
        return self.chain[-1]["hash"] if self.chain else "0"

    def save_chain(self):
        with open("blockchain.json", "w") as file:
            json.dump(self.chain, file, indent=4)
        print("✅ Blockchain successfully saved!")

    def load_chain(self):
        if os.path.exists("blockchain.json"):
            with open("blockchain.json", "r") as file:
                self.chain = json.load(file)
                print("✅ Blockchain successfully loaded!")

blockchain = Blockchain()
