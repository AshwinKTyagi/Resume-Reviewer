import React from "react";
import Layout from "../components/layout";
import { useAuth } from "../context/AuthContext";

const Home = () => {
    const { user } = useAuth();

    return (
        <Layout>
            <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
                <h1 className="text-3xl font-bold mb-4">Resume Reviewer</h1>
                <p className="text-lg">Upload your resume to get a detailed review and feedback or login to see a previously analyzed resume.</p>
                <div className="w-1/2 mt-4 flex space-x-6 item-center">
                    {user ? (
                        <a href="/resume_list" className="w-1/2 p-2 bg-blue-500 text-white text-center rounded mr-2">Resume List</a>
                    ) : (
                        <a href="/login" className="w-1/2 p-2 bg-blue-500 text-white text-center rounded mr-2">Login</a>
                    )}
                    <a className="border-l border-gray-300 mx-2"></a>
                    <a href="/upload" className="w-1/2 p-2 bg-blue-500 text-white text-center rounded">Upload Resume</a>
                </div>
            </div>
        </Layout>
    )
}

export default Home;