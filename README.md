# 🎤 VoiceNote Summarizer

Ứng dụng AI chuyển đổi giọng nói tiếng Việt thành văn bản và tóm tắt nội dung tự động.

**Pipeline:** Ghi âm → Whisper AI (Speech-to-Text) → Ollama LLM (Tóm tắt)

## ✨ Tính năng

- 🎙️ Ghi âm trực tiếp trên trình duyệt
- 🔊 Nhận diện giọng nói tiếng Việt bằng **Whisper** (model `whisper-small-vi`)
- 📝 Tóm tắt nội dung tự động bằng **Ollama** (model `llama3.2`)
- 💾 Tự động lưu trữ file ghi âm

## 🏗️ Kiến trúc

```
AI_TRAINSCRIPT_APP/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── routers/
│   │   ├── trainscripts.py     # API nhận diện giọng nói
│   │   └── summary.py          # API tóm tắt văn bản
│   ├── services/
│   │   ├── whisper_service.py   # Xử lý Whisper STT
│   │   └── ollama_service.py   # Gọi Ollama LLM
│   └── models/                 # Request/Response schemas
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/
│       ├── app.js              # Logic chính
│       ├── api.js              # Gọi API backend
│       └── recorder.js         # Xử lý ghi âm
├── recordings/                 # Thư mục lưu file ghi âm
├── requirements.txt
└── .env
```

## 🛠️ Tech Stack

| Layer    | Công nghệ                                  |
| -------- | ------------------------------------------- |
| Backend  | FastAPI, Uvicorn                            |
| AI / STT | Whisper (`whisper-small-vi` via HuggingFace) |
| AI / LLM | Ollama (`llama3.2`)                         |
| Frontend | HTML, CSS, JavaScript (Vanilla)             |
| Khác     | ffmpeg (convert audio)                      |

## 🚀 Cài đặt & Chạy

### Yêu cầu

- Python 3.10+
- [Ollama](https://ollama.com/) đã cài đặt và chạy model `llama3.2`
- ffmpeg (khuyến nghị, dùng để convert audio)
- GPU (khuyến nghị, giúp Whisper chạy nhanh hơn)

### 1. Clone & cài đặt dependencies

```bash
git clone https://github.com/<your-username>/AI_TRAINSCRIPT_APP.git
cd AI_TRAINSCRIPT_APP

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Cấu hình `.env`

```env
OLLAMA_BASE_URL=http://localhost:11434/api/generate
MODEL_NAME=llama3.2
```

### 3. Khởi động Ollama

```bash
ollama run llama3.2
```

### 4. Chạy Backend

```bash
uvicorn backend.main:app --reload
```

Server chạy tại `http://localhost:8000`

### 5. Mở Frontend

Mở file `frontend/index.html` trên trình duyệt hoặc dùng Live Server.

## 📡 API Endpoints

| Method | Endpoint                    | Mô tả                          |
| ------ | --------------------------- | ------------------------------- |
| POST   | `/api/trainscripts/transcribe` | Upload audio → nhận text        |
| POST   | `/api/summary/`             | Gửi text → nhận bản tóm tắt    |
| GET    | `/`                         | Health check                    |

## 📄 License

MIT
