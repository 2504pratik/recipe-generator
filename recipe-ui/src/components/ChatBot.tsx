import React, { useState, FormEvent } from "react";
import axios from "axios";

interface Message {
  sender: "user" | "bot";
  text: string;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const sendMessage = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Append user message
    const userMessage: Message = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      setLoading(true);
      const response = await axios.post(
        "http://localhost:5005/webhooks/rest/webhook",
        {
          sender: "user",
          message: input,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: false, // Prevents CORS issues
        }
      );

      // Rasa returns an array of responses
      const botMessages = response.data.map((res: any) => ({
        sender: "bot",
        text: res.text,
      }));

      setMessages((prev) => [...prev, ...botMessages]);
    } catch (error) {
      console.error("Error sending message", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Sorry, something went wrong." },
      ]);
    } finally {
      setInput("");
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Recipe Chatbot</h1>
      <div style={styles.chatWindow}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={msg.sender === "user" ? styles.userMessage : styles.botMessage}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <form style={styles.form} onSubmit={sendMessage}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={styles.input}
          disabled={loading}
        />
        <button type="submit" style={styles.button} disabled={loading}>
          Send
        </button>
      </form>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    width: "400px",
    margin: "20px auto",
    border: "1px solid #ccc",
    borderRadius: "8px",
    padding: "16px",
    fontFamily: "Arial, sans-serif",
    backgroundColor: "#f0f0f0",
  },
  header: {
    textAlign: "center",
    marginBottom: "12px",
    color: "#333", 
  },
  chatWindow: {
    height: "400px",
    overflowY: "auto",
    border: "1px solid #eee",
    padding: "8px",
    marginBottom: "12px",
    backgroundColor: "#fff",
  },
  userMessage: {
    textAlign: "right",
    margin: "4px",
    padding: "8px",
    backgroundColor: "#dcf8c6",
    borderRadius: "4px",
    color: "#222",
  },
  botMessage: {
    textAlign: "left",
    margin: "4px",
    padding: "8px",
    backgroundColor: "#f1f0f0",
    borderRadius: "4px",
    color: "#333",
  },
  form: {
    display: "flex",
  },
  input: {
    flex: 1,
    padding: "8px",
    borderRadius: "4px",
    border: "1px solid #ccc",
  },
  button: {
    marginLeft: "8px",
    padding: "8px 16px",
    borderRadius: "4px",
    border: "none",
    backgroundColor: "#007bff",
    color: "#fff",
  },
};

export default Chatbot;