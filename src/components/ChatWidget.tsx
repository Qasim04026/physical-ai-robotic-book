import React, { useState, FormEvent, useEffect } from 'react';
import styles from './ChatWidget.module.css';

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

  useEffect(() => {
    // Scroll to the bottom of the chat window on new message
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
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userMessage.text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botMessage: Message = { text: data.answer, sender: 'bot', sources: data.sources };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to get a response from the chatbot. Please try again later.');
      setMessages((prevMessages) => [...prevMessages, { text: 'Sorry, I am having trouble connecting to the service.', sender: 'bot' }]);
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
            <h3>AI Assistant</h3>
            <button onClick={toggleChat}>X</button>
          </div>
          <div id="chat-window" className={styles.chatWindow}>
            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                <p>{msg.text}</p>
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sources}>
                    <strong>Sources:</strong>
                    <ul>
                      {msg.sources.map((source, srcIndex) => (
                        <li key={srcIndex}>
                          <a href={source} target="_blank" rel="noopener noreferrer">{source}</a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
            {isLoading && <div className={styles.loading}>Bot is typing...</div>}
            {error && <div className={styles.error}>{error}</div>}
          </div>
          <form onSubmit={handleSubmit} className={styles.chatInputForm}>
            <input
              type="text"
              value={input}
              onChange={handleInputChange}
              placeholder="Ask me anything about the book..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>Send</button>
          </form>
        </div>
      )}
    </>
  );
};

export default ChatWidget;
