import RegisterPage from "@/auth/pages/RegisterPage";
import { Route, Routes } from "react-router-dom";
import LoginPage from "@/auth/pages/LoginPage";
import HomePage from "@/app/pages/HomePage";

export const AppRouter = () => {
  return (
    <>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/" element={<HomePage />} />
      </Routes>
    </>
  );
};
