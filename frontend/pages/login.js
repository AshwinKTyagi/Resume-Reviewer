import React, { useState } from 'react';
import Layout from '../components/layout';

const Login = () => {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const handleSubmit = (e) => {
        e.preventDefault()
        console.log({ email, password })
    }

    return (
        <Layout>
            <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
                <div className="p-6 bg-white rounded-lg shadow-lg w-96 text-center">
                    <h2 className="text-2xl font-bold mb-4">Login Page</h2>

                    <form className="mt-6" onSubmit={handleSubmit}>
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

                        <button className="px-4 py-2 bg-blue-500 text-white rounded" type="submit">Login</button>
                    </form>
                </div>
            </div>
        </Layout>
    );
};

export default Login;