import axios from "axios";

// const API_BASE_URL = 'http://127.0.0.1:9511';


const userAPI = axios.create({
    baseURL: '/',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true
})


export const userLogin = (loginData) => {
    return userAPI.post('/api/user_login', loginData);
}

export const userRegister = (registerData) => {
    return userAPI.post('/api/create_user', registerData);
}

export const userUpdate = (updatedData) => {
    return userAPI.put('/api/user_update', updatedData);
}