const BASE_URL = 'http://localhost:8000';

/**
 * Simple auth helper
 * Reads API key from localStorage if present
 */
const auth = {
  get apiKey() {
    return localStorage.getItem('API_KEY');
  },
};

/**
 * Global toast dispatcher (decoupled from UI)
 * UI layer will subscribe in Phase 3.1 (next step)
 */
function dispatchToast(type, message) {
  window.dispatchEvent(
    new CustomEvent('app:toast', {
      detail: { type, message },
    })
  );
}

async function handleResponse(res) {
  if (!res.ok) {
    const text = await res.text();
    const errorMessage = text || 'Request failed';

    // Global error toast
    dispatchToast('error', errorMessage);

    throw new Error(errorMessage);
  }
  return res.json();
}

async function request(method, path, body) {
  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      method,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...(auth.apiKey ? { 'x-api-key': auth.apiKey } : {}),
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });

    const data = await handleResponse(res);
    return data;
  } catch (err) {
    // Network / unexpected error
    dispatchToast('error', err.message || 'Network error');
    throw err;
  }
}

export const apiClient = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body),
};
