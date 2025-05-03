# Ancient DNA Sequence Analysis API

A FastAPI server for analyzing ancient alien DNA sequences, developed for an advanced forensic research team.

## Features

- Upload CSV files containing ancient remains data
- Generate DNA sequences from sample seeds
- Compare DNA sequences between samples
- Natural language Q&A about the API

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload-csv/` | POST | Upload CSV file with sample data |
| `/generate-sequence/` | POST | Generate DNA sequence from sample ID |
| `/compare-sequences/` | POST | Compare two DNA samples |
| `/ask-me-anything/` | GET | Get information about the API |


# 🧬 Ancient DNA Analysis API
This FastAPI application allows users to analyze ancient DNA sequences by uploading CSV data, generating synthetic DNA sequences, comparing them for similarity, and even asking natural-language questions about the API.

# 🚀 Features
📁 Upload CSV files with ancient DNA metadata.

🧬 Generate synthetic DNA sequences based on seed data.

⚖️ Compare DNA sequences for similarity.

🤖 Ask questions using Google's Gemini model (with fallback to local answers).

🛠 Debug endpoints for inspecting internal sample data.

# 📂 Project Structure
bash
ancient_dna_api/
├── main.py                # Main FastAPI app
├── storage.py             # Sample storage handler
├── dna_generator.py       # DNA generation logic
├── models.py              # Pydantic models
├── .env                   # Environment variables (e.g., API key)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

📝 CSV Format
Your uploaded CSV file must contain the following columns:

id — Unique identifier for each DNA sample

region — Geographical region

age — Estimated age

seed — Seed string for DNA generation

Example:

csv
Copy
Edit
id,region,age,seed
001,Mesopotamia,4500,ACGTAGCTAG
002,NileValley,4200,TGCATGCATG
# 🔧 Environment Variables
Create a .env file in the root directory with your Google Gemini API key:

ini
Copy
Edit
GOOGLE_API_KEY=your_google_gemini_api_key

# 📦 Installation & Running Locally


Clone the repository:

bash
Copy
Edit
git clone https://github.com/UmarFarooqMirza/ancient_dna_api.git
cd ancient_dna_api


Create a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the server:

bash
Copy
Edit
uvicorn main:app --reload
# 🧪 API Endpoints
GET /
Check if the API is running.

POST /upload-csv/
Upload a CSV file with DNA sample data.

Form field: file (CSV file)

POST /generate-sequence/
Generate a DNA sequence for a sample ID.

Request Body:

json
Copy
Edit
{
  "id": "001"
}
POST /compare-sequences/
Compare two sample sequences for similarity.

Request Body:

json
Copy
Edit
{
  "id1": "001",
  "id2": "002"
}
GET /ask-me-anything/?question=...
Ask natural language questions about the API.

Example:

bash
Copy
Edit
/ask-me-anything/?question=What data can I upload
GET /debug/samples
View all currently loaded samples and their stats.

GET /debug/sample/{sample_id}
View details of a single sample.


# 🧠 Dependencies
Add these to requirements.txt:
fastapi
uvicorn
python-dotenv
google-generativeai

# 🤖 Powered By
FastAPI

Google Gemini API

Custom K-mer similarity algorithm for sequence comparison
