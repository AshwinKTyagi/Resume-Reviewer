import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';

const Chat = ({ fileId }) => {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);

    const fetchChatHistory = async () => {
        try {
            
            const response = await axios.get(`/api/chat/start-chat?file_id=${fileId}`);
            if (response.data === 0) {
                setMessages((prev) => [...prev, { type: "bot", text: "Hello! How can I help you today?" }]);
            }

            setMessages(response.data);
            
        } catch (error) {
            console.error("Error fetching chat history:", error)
        }
    }

    useEffect(() => {
        if (!fileId) return;
        fetchChatHistory();

    }, [fileId]);

    const handleChat = async () => {
        if (!question.trim()) return;

        setMessages((prev) => [...prev, { type: "user", text: question }]);

        const formData = new FormData();
        formData.append("file_id", fileId);
        formData.append("message", question);

        const response = await axios.post("/api/chat", formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });


        setMessages((prev) => [...prev, { type: "bot", text: response.data.response }]);
        setQuestion("");
    }

    return (
        <div className='flex flex-col p-4 bg-gray-100 h-full w-1/4 shadow-md'>
            <h2 className='text-lg font-bold  flex-shrink-0'>Chat with Your Document</h2>
            <hr className='my-2 border-1' />

            <div className='flex-grow overflow-y-auto bg-gray-300 border p-2 rounded'>
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`p-2 my-1 rounded ${message.type === 'user' ? 'bg-blue-100 text-right' : 'bg-gray-200 text-left'
                            }`}
                    >
                        {message.type === 'bot' ? (
                            <ReactMarkdown className="prose">{message.text}</ReactMarkdown>
                        ) : (
                            message.text
                        )}
                    </div>
                ))}
            </div>
            <div className='flex flex-shrink-0 border p-1'>
                <input
                    type='text'
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    className='border p-2 flex-1'
                />
                <button
                    onClick={handleChat}
                    className='bg-blue-500 text-white p-1 px-4 ml-2 rounded'
                >
                    Send
                </button>
            </div>
        </div>
    );
}

export default Chat;