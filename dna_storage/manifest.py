import json
import time
import os
import uuid

class RunManifest:
    def __init__(self, run_dir="runs"):
        self.run_dir = run_dir
        os.makedirs(run_dir, exist_ok=True)
        self.run_id = time.strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:8]
        self.config = {}
        self.stats = {}
        
    def set_config(self, **kwargs):
        self.config.update(kwargs)
        
    def set_stats(self, **kwargs):
        self.stats.update(kwargs)
        
    def save(self):
        filename = os.path.join(self.run_dir, f"run_{self.run_id}.json")
        data = {
            "run_id": self.run_id,
            "timestamp": time.time(),
            "config": self.config,
            "stats": self.stats
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename
