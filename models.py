from pydantic import BaseModel, Field

class SequenceRequest(BaseModel):
    id: str = Field(..., example="id_0001", 
                   description="Sample ID in format 'id_XXXX'")

class CompareRequest(BaseModel):
    id1: str = Field(..., example="id_0001")
    id2: str = Field(..., example="id_0002")

class AskMeAnythingRequest(BaseModel):
    question: str = Field(..., example="How do I compare sequences?")