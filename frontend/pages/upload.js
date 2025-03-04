import React, { useEffect, useState } from "react"
import axios from "axios"
import { useDropzone } from "react-dropzone"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import remarkBreaks from "remark-breaks"
import Layout from "../components/layout"

const Upload = () => {
    const [resumeText, setResumeText] = useState("");
    const [resumeFeedback, setResumeFeedback] = useState("");
    const [modelOption, setModelOption] = useState("openai")

    useEffect(() => {
        const savedModel = localStorage.getItem("aiModel");
        if (savedModel) setModelOption(savedModel);
    }, []);

    const handleSelect = (model) => {
        const newModel = model;
        localStorage.setItem("aiModel", newModel);
        console.log("Model Option saved in localstorage:", newModel);
        setModelOption(model);
        return model;
    }

    const { getRootProps, getInputProps } = useDropzone({
        accept: {
            "application/pdf": [".pdf"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"]
        },
        onDrop: async (acceptedFiles) => {
            console.log(acceptedFiles[0].type);
            const formData = new FormData();
            const userId = localStorage.getItem("userId");
            
            formData.append("file", acceptedFiles[0]);
            formData.append("modelOption", modelOption);
            if (userId) {
                formData.append("userId", userId);
            }

            try {
                // Send file to backend for extraction
                const response = await axios.post("api/resumes/upload", formData, {
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
        <Layout>
            <div className="h-full flex flex-col items-center justify-center bg-gray-100 p-4 overflow-auto">
                <div className="p-6 bg-white rounded-lg shadow-lg w-96 text-center">
                    <h2 className="text-xl font-bold mb-4">Upload Your Resume</h2>
                    <div {...getRootProps()} className="border-2 border-dashed p-6 cursor-pointer mb-6">
                        <input {...getInputProps()} />
                        <p>Drag and Drop your resume, or click to select a file.</p>
                    </div>
                    <div className="flex flex-col items-center justify-center">
                        <h1 className="text-lrg font-bold mb-6">Select Your AI Model</h1>

                        <div className="flex items-center bg-gray-200 rounded-full p-1 w-48">
                            <button
                                className={`w-1/2 py-2 text-center text-sm font-semibold rounded-full transition ${modelOption === "openai" ? "bg-blue-500 text-white" : "text-gray-500"
                                    }`}
                                onClick={() => handleSelect("openai")}
                            >
                                OpenAI
                            </button>

                            <button
                                className={`w-1/2 py-2 text-center text-sm font-semibold rounded-full transition ${modelOption === "ollama" ? "bg-blue-500 text-white" : "text-gray-500"
                                    }`}
                                onClick={() => handleSelect("ollama")}
                            >
                                Ollama
                            </button>
                        </div>

                        <p className="mt-4 text-gray-700">
                            Selected Model: <strong>{modelOption}</strong>
                        </p>
                    </div>
                </div>

                {resumeText && (
                    <div className="mt-4 p-4 bg-gray-200 rounded">
                        <h3 className="text-xl font-bold">Extracted Text</h3>
                        <pre className="text-sm overflow-auto max-h-40">{resumeText}</pre>
                    </div>
                )}
                {resumeFeedback && (
                    <div className="mt-4 p-4 bg-gray-200 w-3/4 rounded">
                        <ReactMarkdown className="prose prose-lg" remarkPlugins={[remarkGfm, remarkBreaks]}>
                            {resumeFeedback}
                        </ReactMarkdown>
                    </div>
                )}
            </div>
        </Layout>
    );
}

export default Upload;