const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const HEALTH_URL = `${API_BASE_URL}/health`;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export async function waitForBackend({
    retryInterval = 2000,
    timeout = 120000,
} = {}) {
    const start = Date.now();

    while (Date.now() - start < timeout) {
        try {
            const response = await fetch(HEALTH_URL);

            if (response.ok) {
                console.log('backend response');
                return;
            }
        } catch {
            // Ignore and retry
        }

        await sleep(retryInterval);
    }

    return ;
}