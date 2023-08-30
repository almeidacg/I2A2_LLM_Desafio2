document.addEventListener("DOMContentLoaded", function () {
  const chatLog = document.getElementById("chatLog");
  const userInput = document.getElementById("userInput");
  const sendButton = document.getElementById("sendButton");

  sendButton.addEventListener("click", async function () {
      const userMessage = userInput.value.trim();
      if (userMessage !== "") {
          appendMessage("Você", userMessage);
          
          try {
              const response = await sendUserMessageToChatbot(userMessage);
              appendMessage("Azile", response.bot_response);
          } catch (error) {
              console.error("Error:", error);
          }
          
          userInput.value = "";
      }
  });

  async function sendUserMessageToChatbot(message) {
      const response = await fetch("/api/chatbot", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ message })
      });

      if (!response.ok) {
          throw new Error(`Chatbot request failed with status ${response.status}`);
      }

      const responseData = await response.json();
      return responseData;
  }

  function appendMessage(sender, message) {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add("message");
      messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
      chatLog.appendChild(messageDiv);
      chatLog.scrollTop = chatLog.scrollHeight;
  }
});
