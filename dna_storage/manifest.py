import json
import time
import os
import uuid

class RunManifest:
    def __init__(self, base_dir="runs"):
        self.run_id = time.strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:8]
        self.run_dir = os.path.join(base_dir, self.run_id)
        os.makedirs(self.run_dir, exist_ok=True)
        self.config = {}
        self.stats = {}
        
    def set_config(self, **kwargs):
        self.config.update(kwargs)
        
    def set_stats(self, **kwargs):
        self.stats.update(kwargs)
        
    def get_file_path(self, filename):
        return os.path.join(self.run_dir, filename)
        
    def save(self):
        filename = os.path.join(self.run_dir, "manifest.json")
        data = {
            "run_id": self.run_id,
            "timestamp": time.time(),
            "config": self.config,
            "stats": self.stats
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename