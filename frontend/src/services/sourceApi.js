const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getSources(){
    const token = localStorage.getItem('token');
    const result = await fetch(
        `${API_BASE_URL}/sources`,
        {
            method: "GET",
            headers: {
                "Content-Type":
                    "application/json",
                Authorization:`Bearer ${token}`    
            },
        }
    );
    const sources = await result.json()
    return sources;
    
}

export async function connectGoogleDrive() {
    const token = localStorage.getItem('token');
    const response = await fetch(
        `${API_BASE_URL}/sources/google-drive/connect`,
        {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error("Failed to start Google Drive connection");
    }

    const data = await response.json();

    window.location.href = data.authorization_url;
}

export async function disconnectGoogleDrive() {
    const token = localStorage.getItem('token');
    const response = await fetch(
        `${API_BASE_URL}/sources/google-drive`,
        {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error("Failed to disconnect Google Drive");
    }
    return true
}