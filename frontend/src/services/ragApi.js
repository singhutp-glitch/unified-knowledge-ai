import api from "./axiosApi";   // your existing axios instance

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function uploadDocument(file,chatId) {

    const formData = new FormData();

    formData.append("document", file);

    const response = await api.post(
        `/rag/chats/${chatId}/documents`,
        formData
    );

    return response.data;
}


export async function sendRetrievalQuery(currentChatId,userQuery){
     
    const token = localStorage.getItem('token');
    const response = await fetch(
        `${API_BASE_URL}/rag/chats/${currentChatId}/chunks`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json",
                    Authorization:`Bearer ${token}`
            },
            body: JSON.stringify({
                message: userQuery
            }),
        }
    );
    return response.json();
}