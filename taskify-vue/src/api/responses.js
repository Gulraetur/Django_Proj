import api from './axios'

export const createResponse = (taskId, data) => api.post(`/responses/create/${taskId}/`, data)
export const getMyResponses = () => api.get('/responses/my/')
export const getTaskResponses = (taskId) => api.get(`/responses/task/${taskId}/`)
export const acceptRejectResponse = (responseId, action) => api.patch(`/responses/${responseId}/`, { action })