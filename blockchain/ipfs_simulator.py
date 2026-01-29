import hashlib
import json

class IPFSSimulator:
    def __init__(self):
        self.storage = {}
    
    def add_file(self, file_path):
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        file_hash = hashlib.sha256(file_data).hexdigest()
        self.storage[file_hash] = file_path
        
        return f"Qm{file_hash[:44]}"
    
    def add_json(self, data):
        json_str = json.dumps(data, sort_keys=True)
        data_hash = hashlib.sha256(json_str.encode()).hexdigest()
        self.storage[data_hash] = data
        
        return f"Qm{data_hash[:44]}"
    
    def get_file(self, file_hash):
        clean_hash = file_hash.replace('Qm', '')
        return self.storage.get(clean_hash)