// Shared API client placeholder.
export const api = {
  async get<T>(path: string): Promise<T> {
    const res = await fetch(`/api${path}`);
    if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
    return res.json();
  },
};