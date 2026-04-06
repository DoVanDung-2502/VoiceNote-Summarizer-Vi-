from fastapi import APIRouter, HTTPException
from backend.models.request import SummaryRequest
from backend.models.response import SummaryResponse
from backend.services.ollama_service import summarize_text

router = APIRouter()

@router.post("/", response_model=SummaryResponse)
async def summary(request: SummaryRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp nội dung cần tóm tắt")

    summary = await summarize_text(request.text)
    return {"summary": summary}
    
