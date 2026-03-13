from pydantic import BaseModel
from typing import List

class EmailAnalysis(BaseModel):
    subject: str
    sender: str
    category: str  # Urgent, Work, Personal, Newsletter
    summary: str
    action_item: str

class EmailReport(BaseModel):
    analysis: List[EmailAnalysis]
    status: str