import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

async def summarize_text(text: str) -> str:
    prompt = f"Hãy tóm tắt nội dung sau đây một cách ngắn gọn, súc tích bằng tiếng Việt:\n\n{text}"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_BASE_URL, json=payload, timeout=120.0)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "Không thể tạo tóm tắt")
        except Exception as e:
            print(f"Lỗi khi gọi Ollama: {e}")
            return "Lỗi kết nối Ollama"