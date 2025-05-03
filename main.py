from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import csv
from io import StringIO
from storage import storage
from dna_generator import generate_dna_sequence
from models import SequenceRequest, CompareRequest, AskMeAnythingRequest
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = FastAPI(title="Ancient DNA Analysis API",
              description="API for analyzing ancient DNA sequences",
              version="1.0.0")
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("No API key found.")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')  # <-- Correct model name
    print("Gemini model initialized successfully")
except Exception as e:
    print(f"Gemini model initialization failed: {str(e)}")
    model = None
    print("Gemini model not initialized")


@app.get("/")
def root():
    return {"message": "Ancient DNA Analysis API is running"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, detail="Only CSV files are allowed")
    
    try:
        storage.clear()
        content = await file.read()
        decoded = content.decode('utf-8-sig')  # Handle BOM
        reader = csv.DictReader(StringIO(decoded))
        
        for row in reader:
            try:
                storage.add_sample(
                    sample_id=row['id'],
                    region=row['region'],
                    age=row['age'],
                    seed=row['seed']
                )
            except ValueError as e:
                print(f"Skipping invalid row: {str(e)}")
                continue
        
        return {"message": f"Successfully loaded {storage.count_samples()} samples"}
    
    except Exception as e:
        raise HTTPException(500, detail=f"Upload failed: {str(e)}")

@app.post("/generate-sequence/")
def generate_sequence(request: SequenceRequest):
    sample = storage.get_sample(request.id)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample ID not found")

    try:
        # Generate the sequence
        dna_sequence = generate_dna_sequence(
            id=sample['numeric_id'],
            region=sample['region'],
            age=sample['age'],
            dna_seed=sample['seed']
        )
        
        # Get the dominant motif (first 4 characters)
        dominant_motif = dna_sequence[:4] if len(dna_sequence) >= 4 else dna_sequence
        
        return {
            "sample_id": request.id,
            "dna_sequence_beginning": dna_sequence[:100],  # First 100 chars
            "dna_sequence_end": dna_sequence[-100:],       # Last 100 chars
            "length": len(dna_sequence),
            "dominant_motif": dominant_motif,
            "truncated": len(dna_sequence) > 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare-sequences/")
def compare_sequences(request: CompareRequest):
    def calculate_similarity(seq1: str, seq2: str) -> float:
        # Basic similarity calculation using k-mers
        k = 4
        kmers1 = {seq1[i:i+k] for i in range(len(seq1)-k+1)}
        kmers2 = {seq2[i:i+k] for i in range(len(seq2)-k+1)}
        intersection = kmers1 & kmers2
        union = kmers1 | kmers2
        return len(intersection) / len(union) if union else 0.0
    
    sample1 = storage.get_sample(request.id1)
    sample2 = storage.get_sample(request.id2)
    
    if not sample1 or not sample2:
        raise HTTPException(404, detail="One or both sample IDs not found")
    
    seq1 = generate_dna_sequence(
        id=sample1['numeric_id'],
        region=sample1['region'],
        age=sample1['age'],
        dna_seed=sample1['seed']
    )
    
    seq2 = generate_dna_sequence(
        id=sample2['numeric_id'],
        region=sample2['region'],
        age=sample2['age'],
        dna_seed=sample2['seed']
    )
    
    similarity = calculate_similarity(seq1, seq2)
    
    return {
        "sample1": request.id1,
        "sample2": request.id2,
        "similarity_score": similarity,
        "common_region": sample1['region'] == sample2['region']
    }

@app.get("/ask-me-anything/")
async def ask_me_anything(question: str):
    """Hybrid endpoint with automatic fallback"""
    # Local knowledge base as fallback
    local_answers = {
        "what is this server used for": "Analyzing ancient alien DNA sequences",
        "how does this api work": "Upload CSV → Generate Sequences → Compare Samples",
        "what data can i upload": "CSV with: id,region,age,seed",
        "default": "I can answer questions about DNA sequence analysis"
    }

    # Check if model exists
    if model:
        try:
            # If model is initialized, try to get the answer from Gemini API
            response = model.generate_content(
                f"Answer briefly as a DNA API assistant: {question}"
            )
            return {"answer": response.text, "source": "gemini"}
        except Exception as e:
            # If Gemini API fails, print the error and fallback
            print(f"Gemini API failed: {str(e)}")
    
    # Fallback to local answers if model is not available or API call fails
    clean_q = question.lower().strip(' ?')
    return {
        "answer": local_answers.get(clean_q, local_answers["default"]),
        "source": "local"
    }

@app.get("/debug/samples")
def debug_samples():
    samples = {
        k: {
            'region': v['region'],
            'age': v['age'],
            'seed_length': len(v['seed'])
        } 
        for k, v in storage._samples.items()
    }
    return {
        "count": storage.count_samples(),
        "samples": samples
    }
    
@app.get("/debug/samples", include_in_schema=False)
def debug_samples():
    """Debug endpoint to list all loaded samples"""
    return {
        "loaded_samples": len(storage._samples),
        "sample_ids": list(storage._samples.keys())
    }

@app.get("/debug/sample/{sample_id}", include_in_schema=False)
def debug_sample(sample_id: str):
    """Debug endpoint to inspect a specific sample"""
    sample = storage.get_sample(sample_id)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    return sample