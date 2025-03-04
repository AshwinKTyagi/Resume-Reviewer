import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => {
    return useContext(AuthContext);
}

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [uid, setUid] = useState(null);

    useEffect(() => {
        const storedUser = localStorage.getItem("username");
        if (storedUser) {
            setUser(storedUser)
        }
    }, []);

    const login = (userData, token) => {
        localStorage.setItem("username", userData);
        localStorage.setItem("token", token);
        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem("username");
        localStorage.removeItem("token");
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }} >
        { children }
        </AuthContext.Provider>
    )
};

export default AuthContext;