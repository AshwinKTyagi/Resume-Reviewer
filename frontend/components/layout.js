import React from 'react';

const Layout = ({ children }) => {
    return (
        <div>
            <header className='bg-white shadow-md'>
                <div className="container mx-auto flex items-center justify-between p-4">
                    <h1 className="text-3xl font-bold text-gray-900">Resume Reviewer</h1>
                    <nav>
                        <ul className="flex space-x-6 items-center">
                            <li>
                                <a href="/" className="text-gray-700 hover:text-blue-500">Home</a>
                            </li>
                            <li>
                                <a href="/upload" className="text-gray-700 hover:text-blue-500">Upload</a>
                            </li>
                            <li className="border-l border-gray-300 h-6 mx-2"></li>
                            <li>
                                <a href="/login" className="text-gray-700 hover:text-blue-500">Login</a>
                            </li>
                        </ul>
                    </nav>
                </div>
            </header>
            <main>
                {children}
            </main>
            <footer>
                <p>&copy; 2025 Ashwin</p>
            </footer>
        </div>
    );
};

export default Layout;