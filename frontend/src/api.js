// CRA embeds REACT_APP_* values at start/build time.
const baseUrl = (process.env.REACT_APP_API_BASE_URL || 'http://localhost:8001').replace(/\/$/, '');

export const apiUrl = (path) => `${baseUrl}${path}`;
