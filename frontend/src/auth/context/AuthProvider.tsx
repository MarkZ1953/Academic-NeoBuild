import { useNavigate } from "react-router-dom";
import { authReducer } from "./authReducer";
import { useReducer } from "react";
import { AuthContext } from "./AuthContext";
// import { authLogout } from "../services";
import { types } from "../types";
import { toast } from "sonner";

interface AuthProviderProps {
  children: React.ReactNode;
}

const init = () => {
  const user = null;
  return { logged: !!user, user: user };
};

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [authState, dispatch] = useReducer(authReducer, {}, init);
  const navigate = useNavigate();

  const checkSession = () => {};

  const logout = async () => {
    try {
      // const { status } = await authLogout();

      // if (status >= 200 && status < 300) {
      localStorage.clear();
      sessionStorage.clear();
      dispatch({ type: types.LOGOUT });
      toast.success("Sesión cerrada correctamente", { position: "top-center" });
      navigate("/login");
      // }
    } catch (error) {
      toast.error("Error al cerrar sesión", { position: "top-center" });
    }
  };

  return (
    <AuthContext.Provider value={{ ...authState, logout, checkSession }}>
      {children}
    </AuthContext.Provider>
  );
};
