let mediaRecorder;
let audioChunks = [];

// Chọn MIME type mà trình duyệt hỗ trợ (webm/ogg, KHÔNG phải wav)
function getSupportedMimeType() {
    const types = [
        'audio/webm;codecs=opus',
        'audio/webm',
        'audio/ogg;codecs=opus',
        'audio/ogg',
    ];
    for (const type of types) {
        if (MediaRecorder.isTypeSupported(type)) {
            console.log("Sử dụng MIME type:", type);
            return type;
        }
    }
    return ''; // Để trình duyệt tự chọn
}

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mimeType = getSupportedMimeType();
    const options = mimeType ? { mimeType } : {};
    
    mediaRecorder = new MediaRecorder(stream, options);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
            console.log("Nhận chunk âm thanh, size:", event.data.size);
        }
    };

    // timeslice=250ms: đảm bảo ondataavailable được gọi định kỳ
    mediaRecorder.start(250);
    console.log("Đang ghi âm... MIME:", mediaRecorder.mimeType);
}

async function stopRecording() {
    return new Promise((resolve, reject) => {
        mediaRecorder.onstop = () => {
            // Tắt các tracks của microphone để ngắt biểu tượng ghi âm trên trình duyệt
            if (mediaRecorder.stream) {
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
            }

            console.log("Tổng số chunks:", audioChunks.length);
            if (audioChunks.length === 0) {
                reject("Không có dữ liệu âm thanh!");
                return;
            }

            // Dùng đúng mimeType mà recorder đã dùng
            const mimeType = mediaRecorder.mimeType || 'audio/webm';
            const audioBlob = new Blob(audioChunks, { type: mimeType });
            console.log("AudioBlob size:", audioBlob.size, "type:", audioBlob.type);
            resolve(audioBlob);
        };

        if (mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
        }
    });
}