import React from "react";
import ChatInterface from "./components/ChatInterface";
import Hologram from "./components/Hologram";
import "./styles/cybertheme.css";

function App() {
  return (
    <div className="app-container">
      <Hologram />
      <ChatInterface />
    </div>
  );
}

export default App;
