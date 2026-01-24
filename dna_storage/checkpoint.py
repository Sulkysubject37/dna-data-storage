import json
import os

class CheckpointManager:
    def __init__(self, path):
        self.path = path
        
    def load(self):
        if not os.path.exists(self.path):
            return None
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None
            
    def save(self, state):
        tmp_path = self.path + ".tmp"
        with open(tmp_path, 'w') as f:
            json.dump(state, f)
        os.replace(tmp_path, self.path)
