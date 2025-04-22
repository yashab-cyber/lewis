import React, { useState } from "react";

function ChatInterface() {
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);

  const sendMessage = async () => {
    const res = await fetch("http://localhost:5000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    setChatLog([...chatLog, { user: message, bot: data.response }]);
    setMessage("");
  };

  return (
    <div className="chat-box">
      <div className="chat-log">
        {chatLog.map((msg, i) => (
          <div key={i}>
            <p><strong>You:</strong> {msg.user}</p>
            <p><strong>LEWIS:</strong> {msg.bot}</p>
          </div>
        ))}
      </div>
      <input
        type="text"
        placeholder="Type your command..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default ChatInterface;
