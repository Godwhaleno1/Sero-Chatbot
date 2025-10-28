document.getElementById("send-btn").addEventListener("click", sendMessage);

async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  const userText = input.value.trim();
  if (!userText) return;

  // Hiển thị tin nhắn người dùng
  chatBox.innerHTML += `<div class="message user">${userText}</div>`;
  input.value = "";

  // Gửi lên backend
  const response = await fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: userText })
  });

  const data = await response.json();
  chatBox.innerHTML += `<div class="message bot">${data.reply}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}
