import React, { useState } from 'react';
import Layout from '../components/layout';
import { login, register } from '../utils/auth';

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [username, setUsername] = useState("");
    const [isRegister, setIsRegister] = useState(false);
    const [message, setMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (isRegister) {
                await register({ username, email, password });
                setMessage("Registration successful. Please log in.");
                setIsRegister(false);
            } else {
                const response = await login({ email, password });
                setMessage(`Welcome, ${response.user.username}!`);
            }
        } catch (error) {
            if (error.response && error.response.data) {
                setMessage(error.response.data.detail || "An error occurred.");
            } else {
                setMessage("An error occurred. Please try again:" + error.message);
            }
            
        }
    };

    return (
        <Layout>
            <div className="h-full flex flex-col items-center justify-center bg-gray-100 p-4">
                <div className="p-6 bg-white rounded-lg shadow-lg w-96 text-center">
                    <h2 className="text-2xl font-bold mb-4">{isRegister ? "Register" : "Login"}</h2>

                    <form className="mt-6" onSubmit={handleSubmit}>
                        {isRegister && (
                            <div className="p-2 flex justify-between items-center">
                                <label className="w-24 text-left text-gray-700">Username:</label>
                                <input
                                    type="text"
                                    className="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400 ml-4"
                                    placeholder="Enter your username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </div>
                        )}
                        <div className="p-2 flex justify-between items-center">
                            <label className="w-24 text-left text-gray-700">Email:</label>
                            <input
                                type="email"
                                className="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400 ml-4"
                                placeholder="Enter your email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="p-2 flex justify-between items-center">
                            <label className="w-24 text-left text-gray-700">Password:</label>
                            <input
                                type="password"
                                className="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400 ml-4"
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>

                        <button className="px-4 py-2 bg-blue-500 text-white rounded" type="submit">
                            {isRegister ? "Register" : "Login"}
                        </button>
                    </form>

                    <p className="mt-4 text-gray-700">
                        {isRegister ? "Already have an account?" : "Don't have an account?"}
                        <button
                            className="text-blue-500 ml-2"
                            onClick={() => setIsRegister(!isRegister)}
                        >
                            {isRegister ? "Login" : "Register"}
                        </button>
                    </p>

                    {message && <p className="mt-4 text-red-500">{message}</p>}
                </div>
            </div>
        </Layout>
    );
};

export default Login;