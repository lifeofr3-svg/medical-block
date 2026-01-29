from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version
import json
import config

try:
    install_solc('0.8.0')
    set_solc_version('0.8.0')
except Exception as e:
    print(f"Solc installation warning: {e}")

class ContractManager:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(config.GANACHE_URL))
        self.account = config.ACCOUNT_ADDRESS
        self.private_key = config.PRIVATE_KEY
        self.contract = None
        self.contract_address = None

        # Test connection
        if not self.w3.is_connected():
            print(f"WARNING: Cannot connect to blockchain at {config.GANACHE_URL}")
            print("Please check your network configuration.")
        else:
            print(f"✓ Connected to blockchain network")
            print(f"  Network: {config.BLOCKCHAIN_NETWORK}")
            print(f"  Account: {self.account}")
            balance = self.w3.eth.get_balance(self.account)
            eth_balance = self.w3.from_wei(balance, 'ether')
            print(f"  Balance: {eth_balance} ETH")
        
    def compile_and_deploy(self):
        try:
            install_solc('0.8.0', show_progress=True)
            set_solc_version('0.8.0')
        except:
            pass

        # Check balance before deployment
        balance = self.w3.eth.get_balance(self.account)
        eth_balance = self.w3.from_wei(balance, 'ether')
        print(f"Account balance: {eth_balance} ETH")

        if balance == 0:
            raise Exception(
                "Insufficient funds for deployment. "
                "Please add test ETH to your account. "
                "For Sepolia testnet, get test ETH from: https://www.alchemy.com/faucets/ethereum-sepolia"
            )

        with open('contracts/MedicalRecord.sol', 'r') as file:
            contract_source = file.read()

        print("Compiling smart contract...")
        compiled_sol = compile_source(contract_source, output_values=['abi', 'bin'], solc_version='0.8.0')
        contract_id, contract_interface = compiled_sol.popitem()

        abi = contract_interface['abi']
        bytecode = contract_interface['bin']

        MedicalRecord = self.w3.eth.contract(abi=abi, bytecode=bytecode)

        nonce = self.w3.eth.get_transaction_count(self.account)

        print("Building deployment transaction...")
        transaction = MedicalRecord.constructor().build_transaction({
            'from': self.account,
            'nonce': nonce,
            'gas': 3000000,
            'gasPrice': self.w3.eth.gas_price
        })

        print("Signing and sending transaction...")
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(f"Transaction hash: {tx_hash.hex()}")
        print("Waiting for confirmation...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        self.contract_address = tx_receipt.contractAddress
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=abi)

        config.CONTRACT_ADDRESS = self.contract_address
        config.CONTRACT_ABI = abi

        print(f"✓ Contract deployed successfully!")
        print(f"  Contract address: {self.contract_address}")
        print(f"  Block number: {tx_receipt.blockNumber}")
        print(f"  Gas used: {tx_receipt.gasUsed}")

        # Print Etherscan link based on network
        network = config.BLOCKCHAIN_NETWORK
        if network == "sepolia":
            print(f"  View on Etherscan: https://sepolia.etherscan.io/address/{self.contract_address}")
        elif network == "mainnet":
            print(f"  View on Etherscan: https://etherscan.io/address/{self.contract_address}")

        return self.contract_address, abi
    
    def load_contract(self, address, abi):
        self.contract_address = address
        self.contract = self.w3.eth.contract(address=address, abi=abi)
        
    def add_record(self, patient_id, disease_type, prediction, data_hash, image_hash):
        nonce = self.w3.eth.get_transaction_count(self.account)
        
        transaction = self.contract.functions.addRecord(
            patient_id,
            disease_type,
            prediction,
            data_hash,
            image_hash
        ).build_transaction({
            'from': self.account,
            'nonce': nonce,
            'gas': 500000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return tx_hash.hex()
    
    def get_record(self, record_id):
        record = self.contract.functions.getRecord(record_id).call()
        return {
            'patientId': record[0],
            'diseaseType': record[1],
            'prediction': record[2],
            'dataHash': record[3],
            'imageHash': record[4],
            'timestamp': record[5],
            'hospital': record[6]
        }