import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import remarkBreaks from 'remark-breaks';
import Layout from '../components/layout';
import Chat from '../components/chat';


const ResumeList = () => {
    const [resumes, setResumes] = useState([]);
    const [selectedResume, setSelectedResume] = useState("");
    const [resumeText, setResumeText] = useState("");
    const [resumeFeedback, setResumeFeedback] = useState("");

    const fetchResumes = async () => {
        const userId = localStorage.getItem("userId");

        try {
            // Include userId as a query parameter in the request URL
            const response = await axios.get(`/api/resumes?user_id=${userId}`);
            setResumes(response.data);
        } catch (error) {
            console.error("Error fetching resumes:", error);
        }
    };

    useEffect(() => {
        fetchResumes();
    }, []);

    const handleSelectResume = async (resume) => {
        // Retrieve userId from local storage
        const userId = localStorage.getItem("userId");

        // Create a FormData object and append user_id and file_id
        const formData = new FormData();
        formData.append("file_id", resume.id);

        try {
            // Send the FormData to the server
            const response = await axios.post("/api/resumes/file", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // Use the response to set resumeText and resumeFeedback
            setSelectedResume(resume);
            setResumeText(response.data.extracted_text);
            setResumeFeedback(response.data.llm_feedback);
        } catch (error) {
            console.error("Error fetching resume details:", error);
        }
    }

    return (
        <Layout>
            <div className="flex h-full">
                {/* Sidebar */}
                <div className="w-1/4 bg-gray-100 border p-4 shadow-md">
                    <h2 className="text-lg font-bold mb-4">Resumes</h2>

                    {resumes.length > 0 ? (
                        <ul>
                            {resumes.map((resume) => (
                                <li
                                    key={resume.id}
                                    className={`p-2 cursor-pointer ${selectedResume?.id === resume.id ? "bg-blue-100" : "hover:bg-gray-200"
                                        }`}
                                    onClick={() => handleSelectResume(resume)}
                                >
                                    {resume.file_name}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-center text-gray-500">No resumes found.</p>
                    )}
                </div>
                <div className="w-2/4 overflow-auto">
                    {/* Resume Viewer */}
                    <div className="h-full p-6 overflow-auto">
                        {resumeFeedback ? (
                            <div className="mt-4 p-4 bg-gray-200 rounded">
                                <h3 className="text-xl font-bold mb-4">Feedback from LLM</h3>
                                <ReactMarkdown className="prose prose-lg" remarkPlugins={[remarkBreaks, remarkGfm]}>
                                    {resumeFeedback}
                                </ReactMarkdown>
                            </div>
                        ) : (
                            <p className="text-center text-gray-500"></p>
                        )}
                        {resumeText ? (
                            <div className="mt-4 p-4 bg-gray-200 rounded">
                                <h3 className="text-xl font-bold">Extracted Text</h3>
                                <pre className="p-2 text-sm bg-gray-300 overflow-auto max-h-80 rounded">{resumeText}</pre>
                            </div>
                        ) : (
                            <p className="text-center text-gray-500">Select a resume to view</p>
                        )}

                    </div>
                </div>
                    <Chat fileId={selectedResume?.id}></Chat>
            </div>
        </Layout>
    );
}

export default ResumeList;