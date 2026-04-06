from transformers import pipeline
import os
import subprocess
import shutil
import torch
device = 0 if torch.cuda.is_available() else -1
pipe = pipeline("automatic-speech-recognition",
    model="namphungdn134/whisper-small-vi",
    device=device  # đổi thành 0 nếu có GPU
)


def convert_to_wav(input_path: str) -> str:
    """Convert audio file sang WAV để Whisper đọc chính xác hơn.
    Yêu cầu ffmpeg được cài đặt trên hệ thống.
    """
    output_path = input_path.rsplit(".", 1)[0] + "_converted.wav"
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0 and os.path.exists(output_path):
            return output_path
        else:
            print(f"[ffmpeg] Lỗi convert: {result.stderr}")
            return input_path  # fallback: dùng file gốc
    except FileNotFoundError:
        print("[ffmpeg] ffmpeg không được cài đặt, dùng file gốc")
        return input_path
    except Exception as e:
        print(f"[ffmpeg] Lỗi: {e}")
        return input_path

async def transcribe_audio(file_path: str) -> str:
    import asyncio
    converted_path = None
    try:
        # Convert sang WAV nếu file không phải WAV
        if not file_path.lower().endswith(".wav"):
            converted_path = convert_to_wav(file_path)
            process_path = converted_path
        else:
            process_path = file_path
        
        # Chạy Whisper inference trong thread pool để không block event loop
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            lambda: pipe(process_path, generate_kwargs={"language": "vi"})
        )
        return result["text"]
    except Exception as e:
        return f"Lỗi chuyển đổi âm thanh: {str(e)}"
    finally:
        # Xóa file converted tạm (nếu có), file gốc do router quản lý
        if converted_path and converted_path != file_path and os.path.exists(converted_path):
            os.remove(converted_path)
