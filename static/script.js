async function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");
    
    if (userInput.trim() === "") return;
    
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    document.getElementById("user-input").value = "";
    
    let response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    });
    
    let data = await response.json();
    chatBox.innerHTML += `<p><strong>LEWIS:</strong> ${data.LEWIS}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}
