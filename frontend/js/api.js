const API_BASE = "http://localhost:8000/api";

async function uploadAudio(blob) {
    const formData = new FormData();
    // Xác định extension phù hợp từ blob type
    const ext = blob.type.includes("webm") ? ".webm" : blob.type.includes("ogg") ? ".ogg" : ".wav";
    formData.append("file", blob, `recording${ext}`);

    const res = await fetch(`${API_BASE}/trainscripts/transcribe`, {
        method: "POST",
        body: formData
    });

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Lỗi server: ${res.status}`);
    }

    return res.json();
}

async function getSummary(text) {
    const response = await fetch(`${API_BASE}/summary/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Lỗi server: ${response.status}`);
    }

    return await response.json();
}