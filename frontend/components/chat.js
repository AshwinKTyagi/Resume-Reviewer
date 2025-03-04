import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Chat = ({ resumeText }) => {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        if (resumeText) {
            setMessages((prev) => [{ type: "bot", text: "Hello! How can I help you today?" }]);
        }
    }, [resumeText]);

    const handleChat = async () => {
        if (!question.trim()) return;

        setMessages((prev) => [...prev, { type: "user", text: question }]);

        const formData = new FormData();
        formData.append("resume_text", resumeText);
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
        <div className='flex-col p-4 bg-gray-100 h-1/2 overflow-auto'>
            <h2 className='text-lg font-bold mb-2'>Chat with Your Document</h2>

            <div className='overflow-y-auto border p-1'>
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`p-2 my-1 rounded ${message.type === 'user' ? 'bg-blue-200 text-right' : 'bg-gray-200 text-left'
                            }`}
                    >
                        {message.text}
                    </div>
                ))}

                <div className='flex'>
                    <input
                        type='text'
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        className='border p-2 flex-1'
                    />
                    <button
                        onClick={handleChat}
                        className='bg-blue-500 text-white p-2 ml-2 rounded'
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Chat;