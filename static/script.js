js_content = '''
function executeCommand() {
    const command = document.getElementById("command").value;
    fetch("/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerText = data.output;
    });
}
'''

with open("static/script.js", "w") as f:
    f.write(js_content)
