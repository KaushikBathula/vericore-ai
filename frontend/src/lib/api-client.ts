const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiClient {
  static async post<T>(
    endpoint: string,
    data: unknown
  ): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorBody = await response.text();
      throw new Error(
        `API ${response.status}: ${errorBody}`
      );
    }

    return response.json() as Promise<T>;
  }
}