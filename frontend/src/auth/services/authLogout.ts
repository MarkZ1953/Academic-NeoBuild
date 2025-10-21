import API_BASE_URL from "@/config/apiConfig";

/**
 * Sends a logout request to the server.
 *
 * Performs a POST request to `${API_BASE_URL}/auth/logout` with credentials included
 * (cookies are sent). The request includes a "Content-Type: application/json" header
 * but does not send a request body. The function does not parse the response body;
 * it returns only the response HTTP status code.
 *
 * @returns A Promise that resolves to an object with the HTTP status code:
 *          { status: number }.
 *
 * @throws Propagates any error thrown by fetch (e.g., network errors). Note that HTTP
 *         error status codes (4xx/5xx) do not cause a throw — they are returned via
 *         the resolved status value.
 *
 * @remarks
 * - Relies on a runtime-defined API_BASE_URL variable in scope.
 * - Credentials are included to allow cookie-based session invalidation on the server.
 * - Intended to trigger server-side logout behavior (for example, clearing session cookies).
 */
export const authLogout = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/accounts/logout`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });

    return { status: response.status };
  } catch (error) {
    throw error;
  }
};
