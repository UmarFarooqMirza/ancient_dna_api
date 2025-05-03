from typing import Dict, Any
import threading

class SampleStorage:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._samples = {}
        return cls._instance
    
    def add_sample(self, sample_id: str, region: str, age: int, seed: str):
        with self._lock:
            try:
                self._samples[sample_id.lower()] = {
                    'region': region.lower(),
                    'age': int(age),
                    'seed': seed.strip(),
                    'numeric_id': int(sample_id.split('_')[1])
                }
            except (ValueError, IndexError, AttributeError) as e:
                raise ValueError(f"Invalid sample data: {str(e)}")
    
    def get_sample(self, sample_id: str) -> Dict[str, Any]:
        with self._lock:
            return self._samples.get(sample_id.lower())
    
    def count_samples(self) -> int:
        with self._lock:
            return len(self._samples)
    
    def clear(self):
        with self._lock:
            self._samples.clear()

storage = SampleStorage()