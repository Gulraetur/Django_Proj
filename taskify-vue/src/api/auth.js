import api from './axios'

export const login = (username, password) => api.post('/token/', { username, password })
export const register = (data) => api.post('/users/register/', data)
export const getProfile = () => api.get('/users/profile/')
export const updateProfile = (data) => api.put('/users/profile/', data)