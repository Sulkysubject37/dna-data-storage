from ..file_ops import DNAStorage
from .metrics import calculate_overhead, sequence_stats
import time

class SimulationRunner:
    def run_single(self, data, error_model=None, ecc_method='rs', nsym=10, constraints=None, encoding='baseline'):
        storage = DNAStorage(ecc_method, nsym, constraints=constraints, encoding=encoding)
        
        start_time = time.time()
        try:
            encoded = storage.encode(data)
            encode_time = time.time() - start_time
            
            stats = sequence_stats(encoded)
            overhead = calculate_overhead(len(data), len(encoded))
            
            if error_model:
                corrupted = error_model.apply(encoded)
            else:
                corrupted = encoded
            
            start_decode = time.time()
            try:
                decoded = storage.decode(corrupted)
                success = (decoded == data)
            except Exception as e:
                success = False
                decoded = None 
            decode_time = time.time() - start_decode
            
            return {
                "success": success,
                "overhead": overhead,
                "gc": stats['gc'],
                "max_homopolymer": stats['max_homopolymer'],
                "dna_length": len(encoded),
                "encode_time": encode_time,
                "decode_time": decode_time
            }
        except Exception as e:
            return {"error": str(e), "success": False}
