import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

// Use localhost for development, can be configured via docusaurus.config.js customFields in production
const API_BASE_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
  ? null  // Backend not deployed yet - will show demo mode
  : 'http://localhost:8000';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [selectedText, setSelectedText] = useState(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  // Generate session ID on mount
  useEffect(() => {
    setSessionId(generateSessionId());
  }, []);

  // Listen for text selection events
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text.length > 10) { // Only capture meaningful selections
        setSelectedText(text);
        setIsOpen(true); // Open chatbot when text is selected

        // Add a system message
        setMessages(prev => [...prev, {
          type: 'system',
          content: `Text selected: "${text.substring(0, 100)}${text.length > 100 ? '...' : ''}"`
        }]);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  const generateSessionId = () => {
    return 'session_' + Math.random().toString(36).substr(2, 9);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');

    // Add user message to chat
    setMessages(prev => [...prev, {
      type: 'user',
      content: userMessage,
      timestamp: new Date()
    }]);

    setIsLoading(true);

    try {
      // Check if backend is available
      if (!API_BASE_URL) {
        // Demo mode - backend not deployed yet
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate delay

        setMessages(prev => [...prev, {
          type: 'bot',
          content: `🤖 **Demo Mode Active**\n\nThe RAG chatbot backend is currently not deployed. This is a fully functional UI with the following features ready:\n\n✅ Complete chatbot interface\n✅ Selected text query support\n✅ FastAPI backend code (in /backend directory)\n✅ OpenAI + Qdrant + SQLite integration ready\n\n**Your question:** "${userMessage}"\n\n**To activate:**\n1. Deploy the backend from /backend directory\n2. Update API_BASE_URL in src/components/Chatbot/index.js\n3. Rebuild and redeploy\n\n📚 See CHATBOT_SETUP.md for full instructions.`,
          timestamp: new Date()
        }]);

        setIsLoading(false);
        if (selectedText) {
          setSelectedText(null);
        }
        return;
      }

      // Determine endpoint based on whether we have selected text
      const endpoint = selectedText
        ? `${API_BASE_URL}/api/chat/selected`
        : `${API_BASE_URL}/api/chat`;

      const requestBody = selectedText
        ? {
            query: userMessage,
            selected_text: selectedText,
            session_id: sessionId
          }
        : {
            query: userMessage,
            session_id: sessionId
          };

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error('Failed to get response from chatbot');
      }

      const data = await response.json();

      // Add bot response to chat
      setMessages(prev => [...prev, {
        type: 'bot',
        content: data.answer,
        timestamp: new Date(),
        sources: data.retrieved_chunks
      }]);

      // Clear selected text after using it
      if (selectedText) {
        setSelectedText(null);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        type: 'error',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearSelectedText = () => {
    setSelectedText(null);
    setMessages(prev => prev.filter(msg => msg.type !== 'system'));
  };

  return (
    <>
      {/* Chatbot Toggle Button */}
      <button
        className={styles.chatbotToggle}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chatbot"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chatbot Window */}
      {isOpen && (
        <div className={styles.chatbotWindow}>
          {/* Header */}
          <div className={styles.chatbotHeader}>
            <div className={styles.headerTitle}>
              <span className={styles.headerIcon}>🤖</span>
              <span>Physical AI Assistant</span>
            </div>
            <button
              className={styles.closeButton}
              onClick={() => setIsOpen(false)}
              aria-label="Close chatbot"
            >
              ✕
            </button>
          </div>

          {/* Selected Text Indicator */}
          {selectedText && (
            <div className={styles.selectedTextBanner}>
              <div className={styles.selectedTextContent}>
                <span className={styles.selectedTextLabel}>Selected text:</span>
                <span className={styles.selectedTextPreview}>
                  {selectedText.substring(0, 100)}
                  {selectedText.length > 100 ? '...' : ''}
                </span>
              </div>
              <button
                className={styles.clearSelectionButton}
                onClick={clearSelectedText}
                aria-label="Clear selection"
              >
                ✕
              </button>
            </div>
          )}

          {/* Messages Container */}
          <div className={styles.messagesContainer}>
            {messages.length === 0 && (
              <div className={styles.welcomeMessage}>
                <p>👋 Welcome! I'm your AI assistant for this coursebook.</p>
                {!API_BASE_URL ? (
                  <>
                    <p>🤖 <strong>Demo Mode:</strong> The chatbot UI is fully functional, but the backend is not yet deployed.</p>
                    <p className={styles.tip}>
                      💡 Try asking a question to see the demo response and setup instructions!
                    </p>
                  </>
                ) : (
                  <>
                    <p>Ask me anything about Physical AI and Humanoid Robotics!</p>
                    <p className={styles.tip}>
                      💡 Tip: Select any text on the page and ask me questions about it.
                    </p>
                  </>
                )}
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={`${styles.message} ${styles[message.type]}`}
              >
                {message.type === 'system' && (
                  <div className={styles.systemMessage}>
                    ℹ️ {message.content}
                  </div>
                )}

                {message.type === 'user' && (
                  <div className={styles.userMessage}>
                    {message.content}
                  </div>
                )}

                {message.type === 'bot' && (
                  <div className={styles.botMessage}>
                    <div className={styles.botContent}>
                      {message.content}
                    </div>
                    {message.sources && message.sources.length > 0 && (
                      <div className={styles.sources}>
                        <details>
                          <summary className={styles.sourcesToggle}>
                            📚 Sources ({message.sources.length})
                          </summary>
                          <div className={styles.sourcesList}>
                            {message.sources.map((source, idx) => (
                              <div key={idx} className={styles.sourceItem}>
                                <span className={styles.sourceTitle}>
                                  {source.metadata.title || 'Unknown'}
                                </span>
                                <span className={styles.sourceScore}>
                                  Match: {(source.score * 100).toFixed(0)}%
                                </span>
                              </div>
                            ))}
                          </div>
                        </details>
                      </div>
                    )}
                  </div>
                )}

                {message.type === 'error' && (
                  <div className={styles.errorMessage}>
                    ⚠️ {message.content}
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className={styles.message}>
                <div className={styles.loadingMessage}>
                  <span className={styles.loadingDots}>●●●</span>
                  <span>Thinking...</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className={styles.inputContainer}>
            <textarea
              className={styles.messageInput}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={selectedText ? "Ask about the selected text..." : "Ask me anything..."}
              rows="2"
              disabled={isLoading}
            />
            <button
              className={styles.sendButton}
              onClick={sendMessage}
              disabled={!inputValue.trim() || isLoading}
              aria-label="Send message"
            >
              {isLoading ? '⏳' : '➤'}
            </button>
          </div>
        </div>
      )}
    </>
  );
}
