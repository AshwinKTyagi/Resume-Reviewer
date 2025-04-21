import axios from "axios";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";

export const useAuth = () => useContext(AuthContext);

export const register = async (userData) => {
    console.log("Register payload:", userData);
    
    return await axios.post("api/auth/register", userData);
}

export const login = async (userData) => {
    const response = await axios.post("api/auth/login", userData);
    if (response.data.access_token) {
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("username", response.data.user.username);
        localStorage.setItem("userId", response.data.user.user_id);
    }
    return response.data;
}

export const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("userId");
}
