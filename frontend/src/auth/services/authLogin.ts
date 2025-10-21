import API_BASE_URL from "@/config/apiConfig";

interface LoginParams {
  username: string;
  password: string;
}

/**
 * Authenticate a user by sending their credentials to the backend login endpoint.
 *
 * Performs a POST request to `${API_BASE_URL}/auth/login` with a JSON body
 * containing { username, password } and includes credentials (cookies) in the request.
 *
 * @param username - The username (or identifier) of the user to authenticate.
 * @param password - The user's plaintext password.
 * @returns A promise that resolves to an object with:
 *  - status: The HTTP status code returned by the server.
 *  - data: The parsed JSON response body from the server.
 *
 * @throws Will rethrow any network or JSON parsing errors encountered during fetch or response.json().
 */
export const authLogin = async ({ username, password }: LoginParams) => {
  try {
    const response = await fetch(`${API_BASE_URL}/accounts/login`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    return { status: response.status, data: await response.json() };
  } catch (error) {
    throw error;
  }
};
