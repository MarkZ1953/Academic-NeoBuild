import { createContext } from "react";

export interface AuthContextType {
  logged: boolean;
  user: any | null;
  logout: () => Promise<void>;
  checkSession: () => void;
}

export const AuthContext = createContext<AuthContextType>(
  {} as AuthContextType
);
