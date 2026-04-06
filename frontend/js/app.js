const recordBtn = document.getElementById("recordBtn");
const status = document.getElementById("status");
const transcriptBox = document.getElementById("transcript");
const summaryBox = document.getElementById("summary");

let isRecording = false;

function setStatus(message, type = "info") {
    status.innerText = message;
    status.className = `status-${type}`;
}

function resetUI() {
    isRecording = false;
    recordBtn.innerText = "🎙️ Nhấn để ghi âm";
    recordBtn.disabled = false;
    recordBtn.classList.remove("recording");
}

recordBtn.addEventListener("click", async () => {
    if (!isRecording) {
        // Bắt đầu ghi âm
        try {
            await startRecording();
            isRecording = true;
            recordBtn.innerText = "⏹️ Dừng ghi âm";
            recordBtn.classList.add("recording");
            setStatus("🔴 Đang ghi âm...", "recording");
            transcriptBox.innerText = "...";
            summaryBox.innerText = "...";
        } catch (err) {
            console.error("Lỗi khi bắt đầu ghi âm:", err);
            setStatus("❌ Không thể truy cập microphone", "error");
            resetUI();
        }
    } else {
        // Dừng ghi âm và xử lý
        recordBtn.disabled = true;
        recordBtn.innerText = "⏳ Đang xử lý...";
        recordBtn.classList.remove("recording");

        try {
            // Bước 1: Dừng ghi âm
            setStatus("⏳ Đang dừng ghi âm...", "processing");
            const audioBlob = await stopRecording();
            console.log("Audio blob:", audioBlob.size, "bytes, type:", audioBlob.type);

            if (!audioBlob || audioBlob.size === 0) {
                throw new Error("Không có dữ liệu âm thanh");
            }

            // Bước 2: Gửi lên backend để nhận diện giọng nói (Whisper)
            setStatus("🔄 Đang nhận diện giọng nói...", "processing");
            transcriptBox.innerHTML = '<span class="loading">Đang xử lý...</span>';
            
            const trainscriptData = await uploadAudio(audioBlob);

            if (!trainscriptData || !trainscriptData.text) {
                throw new Error(trainscriptData?.detail || "Không có văn bản trả về từ mô hình nhận diện giọng nói");
            }

            // Hiển thị văn bản nhận diện
            transcriptBox.innerText = trainscriptData.text;
            console.log("Transcript:", trainscriptData.text);

            // Bước 3: Gửi text sang API tóm tắt (Ollama)
            setStatus("📝 Đang tóm tắt nội dung...", "processing");
            summaryBox.innerHTML = '<span class="loading">Đang tóm tắt...</span>';
            
            const summaryData = await getSummary(trainscriptData.text);

            if (!summaryData || !summaryData.summary) {
                throw new Error("Không nhận được bản tóm tắt");
            }

            // Hiển thị tóm tắt
            summaryBox.innerText = summaryData.summary;
            console.log("Summary:", summaryData.summary);

            setStatus("✅ Hoàn tất!", "success");

        } catch (error) {
            console.error("Lỗi xử lý:", error);
            setStatus(`❌ Lỗi: ${error.message}`, "error");
            
            // Đảm bảo hiển thị lỗi trong các box nếu chưa có nội dung
            if (transcriptBox.innerText === "..." || transcriptBox.querySelector(".loading")) {
                transcriptBox.innerText = "Không thể nhận diện";
            }
            if (summaryBox.innerText === "..." || summaryBox.querySelector(".loading")) {
                summaryBox.innerText = "Không thể tóm tắt";
            }
        } finally {
            resetUI();
        }
    }
});