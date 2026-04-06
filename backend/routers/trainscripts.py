# import shutil
# from fastapi import APIRouter
# from backend.models.request import SummaryRequest
# from backend.models.response import TranscriptResponse
# from fastapi import APIRouter, UploadFile, File, HTTPException
# import shutil
# import os

# router = APIRouter()

# @router.post("/transcribe", response_model=TranscriptResponse)
# async def transcribe(file: UploadFile = File(...)):
#     temp_file_path = f"temp_{file.filename}"
#     with open(temp_file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     text = await transcribe_audio(temp_file_path)
#     if not text:
#         raise HTTPException(status_code=500, detail="Không thể tạo bản chép")
#     return {"text": text.strip()}

from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.whisper_service import transcribe_audio
import shutil
import os
import uuid
from datetime import datetime

router = APIRouter()

# Thư mục lưu file ghi âm
RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

def get_extension_from_content_type(content_type: str) -> str:
    """Lấy extension phù hợp từ MIME type của file upload"""
    mapping = {
        "audio/webm": ".webm",
        "audio/ogg": ".ogg",
        "audio/wav": ".wav",
        "audio/mpeg": ".mp3",
        "audio/mp4": ".mp4",
        "audio/x-m4a": ".m4a",
    }
    ct = content_type.split(";")[0].strip().lower()
    return mapping.get(ct, ".webm")  # mặc định .webm

@router.post("/transcribe")
async def api_transcript(file: UploadFile = File(...)):
    # Xác định extension đúng theo content-type
    ext = get_extension_from_content_type(file.content_type or "audio/webm")
    unique_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
    
    # Đường dẫn file tạm để Whisper xử lý
    temp_file = f"temp_{unique_id}{ext}"
    # Đường dẫn lưu bản ghi âm
    saved_file = os.path.join(RECORDINGS_DIR, f"recording_{unique_id}{ext}")
    
    try:
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="File âm thanh rỗng, vui lòng thử lại")
        
        # Lưu file tạm để Whisper xử lý
        with open(temp_file, "wb") as buffer:
            buffer.write(file_content)
        
        # Lưu bản sao vào thư mục recordings
        with open(saved_file, "wb") as buffer:
            buffer.write(file_content)
        
        print(f"[Transcribe] Nhận file: {file.filename}, size: {len(file_content)} bytes, type: {file.content_type}")
        print(f"[Transcribe] Đã lưu ghi âm: {saved_file}")
        
        # Gọi service Whisper để nhận diện
        text = await transcribe_audio(temp_file)
        
        if not text:
            raise HTTPException(status_code=500, detail="Không thể nhận diện giọng nói")
        
        if text.startswith("Lỗi chuyển đổi âm thanh:"):
            raise HTTPException(status_code=500, detail=text)
            
        return {"text": text.strip(), "saved_file": saved_file}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")
    finally:
        # Chỉ xóa file TẠM, giữ lại file trong recordings/
        if os.path.exists(temp_file):
            os.remove(temp_file)