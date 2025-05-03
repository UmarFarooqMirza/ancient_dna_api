import random
from functools import lru_cache

def generate_dna_sequence(id: int, region: str, age: int, dna_seed: str) -> str:
    """Generate DNA sequence from seed data.
    
    Args:
        id: Sample numeric ID
        region: One of ['apac', 'na', 'latam', 'emea']
        age: Sample age in years
        dna_seed: Seed string containing genetic motifs
        
    Returns:
        Generated DNA sequence (length 1,010,101,010)
        or raises ValueError for invalid inputs
    """
    random.seed(f"{id}+{region}+{age}")
    
    # Region-specific motifs
    MOTIFS = {
        "apac": ["agtc", "agct", "actg", "atgc"],
        "na": ["gtac", "gcat", "gcta"],
        "latam": ["cgta", "ctga", "catg"],
        "emea": ["aagt", "aatg", "aagc"]
    }
    
    if region.lower() not in MOTIFS:
        raise ValueError(f"Invalid region: {region}")
    
    def find_motifs(seed: str) -> list:
        seed_lower = seed.lower()
        return [
            seed_lower[i:i+4]
            for i in range(0, len(seed_lower)-3, 4)
            if seed_lower[i:i+4] in MOTIFS[region.lower()]
        ]
    
    @lru_cache(maxsize=100)
    def _expensive_computation():
        x = 1
        for _ in range(100_000):  # Simulate expensive computation
            x = (x * 987654321) % 123456789
        return x
    
    TARGET_LENGTH = 1010101010
    sequence_parts = []
    current_length = 0
    
    while current_length < TARGET_LENGTH:
        _expensive_computation()
        valid_motifs = find_motifs(dna_seed)
        
        if not valid_motifs:
            raise ValueError("No valid motifs found in seed")
        
        chosen_motif = random.choice(valid_motifs)
        repeat_count = random.randint(10**3, 10**5)
        repeated_seq = chosen_motif * repeat_count
        sequence_parts.append(repeated_seq)
        current_length += len(repeated_seq)
    
    return "".join(sequence_parts)[:TARGET_LENGTH]