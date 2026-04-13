import ReactMarkdown from 'react-markdown';
import React, { useState, FormEvent, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import styles from './ChatWidget.module.css';   // ← Yeh line zaroori hai

interface Message {
  text: string;
  sender: 'user' | 'bot';
  sources?: string[];
}

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Session ID generate once
  const [session_id] = useState<string>(uuidv4());

  // Auto scroll to bottom
  useEffect(() => {
    const chatWindow = document.getElementById('chat-window');
    if (chatWindow) {
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }
  }, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (input.trim() === '') return;

    const userMessage: Message = { text: input, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);

    const currentInput = input;
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const API_BASE_URL = 'https://qasim-robotic-physical-ai-chatbot.hf.space';

      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          question: currentInput,
          session_id: session_id 
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage: Message = { 
        text: data.answer, 
        sender: 'bot',
        sources: data.sources || [] 
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to get response. Please try again.');
      setMessages((prev) => [...prev, { 
        text: "Sorry, I'm having trouble connecting right now. Please try again.", 
        sender: 'bot' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <button className={styles.chatButton} onClick={toggleChat}>
        {isOpen ? 'Close Chat' : 'Open Chat'}
      </button>

      {isOpen && (
        <div className={styles.chatContainer}>
          <div className={styles.chatHeader}>
            <h3>🤖 Robotics Book Assistant</h3>
            <button onClick={toggleChat}>✕</button>
          </div>

          <div id="chat-window" className={styles.chatWindow}>
            {/* Welcome Message - English by default */}
            {messages.length === 0 && (
              <div className={styles.welcome}>
                👋 Hello!<br />
                I'm your Physical AI Robotics book assistant.<br />
                Ask me anything about the book!
              </div>
            )}

            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                <ReactMarkdown>{msg.text}</ReactMarkdown>
                
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sources}>
                    <strong>Sources:</strong>
                    <ul>
                      {msg.sources.map((source, i) => (
                        <li key={i}>
                          <a href={source} target="_blank" rel="noopener noreferrer">{source}</a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}

            {isLoading && <div className={styles.loading}>Thinking...</div>}
            {error && <div className={styles.error}>{error}</div>}
          </div>

          <form onSubmit={handleSubmit} className={styles.chatInputForm}>
            <input
              type="text"
              value={input}
              onChange={handleInputChange}
              placeholder="Ask anything about the book..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>
              Send
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default ChatWidget;