import { RegisterForm } from "../components";

const RegisterPage = () => {
  return (
    <>
      <div className="bg-muted flex min-h-svh flex-col items-center justify-center p-6 md:p-8">
        <div className="max-w-sm">
          <RegisterForm />
        </div>
      </div>
    </>
  );
};

export default RegisterPage;
