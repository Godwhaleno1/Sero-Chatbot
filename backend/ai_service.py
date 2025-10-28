import os
from google import genai

os.environ["GEMINI_API_KEY"] = "AIzaSyDmSMjaj7d1m_CnG41ceysp3dEYTbj5kNk"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def load_private_knowledge(file_path: str = None) -> str:
    """
    Đọc nội dung tài liệu nội bộ (nếu có).
    Nếu không truyền file_path, trả về nội dung mẫu.
    """
    if file_path and os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    # Nội dung mặc định nếu không có file
    return """
    Tài liệu nội bộ:
    - Liệu pháp CBT giúp người bị lo âu học cách thay đổi suy nghĩ tiêu cực.
    - Ngủ đủ giấc (7-8 tiếng) và tập thể dục 30 phút mỗi ngày giảm stress hiệu quả.
    - Không nên dùng chất kích thích khi đang điều trị trầm cảm.
    """

# 📘 1️⃣ Hàm chính sinh phản hồi AI
def generate_ai_reply(prompt: str, context_file: str = None) -> str:
    """
    Sinh phản hồi từ Gemini Flash, kết hợp system_instruction + context riêng.
    """
    try:
        # Nạp dữ liệu (context injection)
        context = load_private_knowledge(context_file)

        # Tạo nội dung tổng hợp cho prompt
        full_prompt = f"""
        Dựa vào tài liệu sau đây, hãy trả lời câu hỏi của người dùng.

        --- Tài liệu ---
        {context}

        --- Câu hỏi ---
        {prompt}
        --- Kết hợp ---
        Bạn là chatbot tư vấn sức khỏe tâm lý.
    Luôn trả lời nhẹ nhàng, có cảm xúc, và khích lệ người dùng.
    Dùng tiếng Việt tự nhiên, tránh giọng máy móc.
    Khi có thể, hãy gợi ý thêm hoạt động giúp cải thiện tinh thần (ví dụ: thiền, thể thao, viết nhật ký...).
        """

        # Gọi Gemini Flash với system instruction
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )

        # resp có thể chứa nhiều phần, nhưng text chính nằm ở resp.text
        return resp.text.strip() if resp.text else "Xin lỗi, tôi chưa thể trả lời câu hỏi này."
    except Exception as e:
        print("❌ Lỗi khi gọi Gemini API:", e)
        return "Xin lỗi, tôi gặp lỗi khi kết nối tới mô hình AI."
