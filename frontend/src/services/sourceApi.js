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

export async function getPickerToken(){
    const token = localStorage.getItem("token");
        const response = await fetch(
            `${API_BASE_URL}/sources/google-drive/picker-token`,
            {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Failed to get Google Drive access token");
        }

        const data = await response.json();
        return data
}

export async function putRootFolderId(folderId){
    const token = localStorage.getItem("token")
    const response = await fetch(
        `${API_BASE_URL}/sources/google-drive/root-folder`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                Authorization:
                    `Bearer ${token}`
            },

            body: JSON.stringify({
                folder_id: folderId
            })
        }
    );

    if (!response.ok) {
        throw new Error(
            "Failed to save root folder"
        );
    }

    const data = await response.json();
    return data;
    
}


export async function removeRootFolder(){
    const token = localStorage.getItem("token")
    const response = await fetch(
        `${API_BASE_URL}/sources/google-drive/root-folder`,
        {
            method: "DELETE",

            headers: {
                "Content-Type": "application/json",
                Authorization:
                    `Bearer ${token}`
            },
        }
    );

    if (!response.ok) {
        throw new Error(
            "Failed to remove root folder"
        );
    }

    const data = await response.json();
    return data;
    
}



export async function getRootFolder(){
    const token = localStorage.getItem("token")
    const response = await fetch(
        `${API_BASE_URL}/sources/google-drive/root-folder`,
        {
            method: "GET",

            headers: {
                "Content-Type": "application/json",
                Authorization:
                    `Bearer ${token}`
            },
        }
    );

    if (!response.ok) {
        throw new Error(
            "Failed to get root folder"
        );
    }

    const data = await response.json();
    return data;
    
}

export async function getCheckoutChanges(){
    const token = localStorage.getItem("token")
    const response = await fetch(
        `${API_BASE_URL}/sources/google-drive/changes`,
        {
            method: "GET",

            headers: {
                "Content-Type": "application/json",
                Authorization:
                    `Bearer ${token}`
            },
        }
    );

    if (!response.ok) {
        throw new Error(
            "Failed to get drive changes"
        );
    }

    const data = await response.json();
    return data;
    
}

export async function syncAllCheckoutChanges(payload){
    const token = localStorage.getItem("token");
    const response = await fetch(
        `${API_BASE_URL}/sources/google-drive/sync`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                Authorization:
                    `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        }
    );

    if (!response.ok) {
        throw new Error(
            "Failed to start syncing changes"
        );
    }
    const data = await response.json();
    return data;
    
}

export async function getActiveSyncJob(){
    const token = localStorage.getItem("token");
    const response = await fetch(
        `${API_BASE_URL}/sources/google-drive/active-sync`,
        {
            method: "GET",

            headers: {
                "Content-Type": "application/json",
                Authorization:
                    `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error(
            "Failed to start syncing changes"
        );
    }
    const data = await response.json();
    return data;
    
}


export async function getSyncStatus(jobId){
    const token = localStorage.getItem("token");
    const response = await fetch(
        `${API_BASE_URL}/sources/google-drive/sync-status/${jobId}`,
        {
            method: "GET",

            headers: {
                "Content-Type": "application/json",
                Authorization:
                    `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error(
            "Failed to start syncing changes"
        );
    }
    const data = await response.json();
    return data;
    
}


