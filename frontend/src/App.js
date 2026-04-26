import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [tab, setTab] = useState("form");
  const [loading, setLoading] = useState(false);
  // Form states
  const [income, setIncome] = useState("");
  const [occupation, setOccupation] = useState("");
  const [category, setCategory] = useState("");
  const [result, setResult] = useState([]);

  // Chat states
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  // 🔹 FORM SUBMIT
  const handleForm = async () => {
  setLoading(true);
  const res = await axios.post("http://localhost:5000/recommend", {
    income: Number(income),
    occupation,
    category,
  });
  setResult(res.data.schemes);
  setLoading(false);
};
{loading && <p style={{textAlign:"center"}}>🔍 Finding best schemes...</p>}
  // 🔹 CHAT SEND
  const sendMessage = async () => {
    if (!message) return;

    const newChat = [...chat, { sender: "user", text: message }];
    setChat(newChat);

    const res = await axios.post("http://localhost:5000/chat", {
      message,
    });

    setChat([
      ...newChat,
      { sender: "bot", text: res.data.reply },
    ]);

    setMessage("");
  };

  return (
    <div className="container">
      <h1>AI Scheme Assistant</h1>

      {/* 🔹 Tabs */}
      <div className="tabs">
        <button onClick={() => setTab("form")}>Form</button>
        <button onClick={() => setTab("chat")}>Chatbot</button>
      </div>

      {/* 🔹 FORM UI */}
      {tab === "form" && (
        <>
          <input
            placeholder="Income"
            onChange={(e) => setIncome(e.target.value)}
          />

          <select onChange={(e) => setOccupation(e.target.value)}>
            <option>Occupation</option>
            <option>Student</option>
            <option>Farmer</option>
            <option>Unemployed</option>
            <option>Any</option>
          </select>

          <select onChange={(e) => setCategory(e.target.value)}>
            <option>Category</option>
            <option>Education</option>
            <option>Agriculture</option>
            <option>Health</option>
            <option>Employment</option>
          </select>

          <button onClick={handleForm}>Get Schemes</button>

          {/* 🔥 RESULT DASHBOARD */}
          <div className="results">
           {result.map((r, i) => (
  <div key={i} className="card">
    <h3>{r.name}</h3>
    <p><b>Category:</b> {r.category}</p>
    <p><b>Benefit:</b> {r.benefit}</p>
    <p><b>Description:</b> {r.description}</p>
    <p><b>Why Eligible:</b> {r.reason}</p>
  </div>
))}
          </div>
        </>
      )}

      {/* 🔹 CHATBOT UI */}
      {tab === "chat" && (
        <>
          <div className="chatbox">
            {chat.map((msg, i) => (
              <div key={i} className={msg.sender}>
                {msg.text}
              </div>
            ))}
          </div>

          <div className="inputBox">
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask something..."
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </>
      )}
    </div>
  );
}

export default App;