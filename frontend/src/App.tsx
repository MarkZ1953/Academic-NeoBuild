import { Toaster } from "@/components/ui/sonner";
import { AppRouter } from "./router/AppRouter";
import { AuthProvider } from "./auth/context";

function App() {
  return (
    <>
      <AuthProvider>
        <AppRouter />
      </AuthProvider>
      <Toaster />
    </>
  );
}

export default App;
