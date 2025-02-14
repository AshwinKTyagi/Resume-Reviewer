import React, { useState } from "react"
import axios from "axios"
import { useDropzone } from "react-dropzone"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

export default function Home() {
    const[resumeText, setResumeText] = useState("");
    const[resumeFeedback, setResumeFeedback] = useState("");
    const { getRootProps, getInputProps } = useDropzone({
        accept: {
            "application/pdf": [".pdf"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"]
        },
        onDrop: async (acceptedFiles) => {
            console.log(acceptedFiles[0].type);
            const formData = new FormData();
            formData.append("file", acceptedFiles[0]);
            
            try {
                // Send file to backend for extraction
                const response = await axios.post("api/upload/", formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
                setResumeText(response.data.extracted_text); // Set extracted text to state
                setResumeFeedback(response.data.llm_feedback); // Set feedback from LLM to state
            } catch (error) {
                console.error("Error uploading file:", error); // Handle error
            }
        },
    });

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
            <div className="p-6 bg-white rounded-lg shadow-lg w-96 text-center">
                <h2 className="text-xl font-bold mb-4">Upload Your Resume</h2>
                <div {...getRootProps()} className="border-2 border-dashed p-6 cursor-pointer">
                    <input {...getInputProps()} />
                    <p>Drag and Drop your resume, or click to select a file.</p>
                </div>
                
            </div>
            {resumeText && (
                <div className="mt-4 p-4 bg-gray-200 rounded">
                    <h3 className="text-xl font-bold">Extracted Text</h3>
                    <pre className="text-sm overflow-auto max-h-40">{resumeText}</pre>
                </div>
            )}
            {resumeFeedback && (
                <div className="mt-4 p-4 bg-gray-200 w-screen rounded">
                    <h3 className="text-xl font-bold mb-4">Feedback from LLM</h3>
                    <ReactMarkdown className="prose prose-lg" remarkPlugins={[remarkGfm]}>
                        {resumeFeedback}
                    </ReactMarkdown>
                </div>
            )}
        </div>
    );
}