import { Card, CardContent } from "@/components/ui/card";
import { yupResolver } from "@hookform/resolvers/yup";
import { Link, useNavigate } from "react-router-dom";
import { Spinner } from "@/components/ui/spinner";
import { authLoginSchema } from "@/auth/schemas";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useEffect, useState } from "react";
import { authLogin } from "@/auth/services";
import { useForm } from "react-hook-form";
import { CircleX } from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import * as yup from "yup";

import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field";

type LoginFormData = yup.InferType<typeof authLoginSchema>;

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const logged = false;

  useEffect(() => {
    if (logged) {
      navigate("/");
    }
  }, [logged, navigate]);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: yupResolver(authLoginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      setIsLoading(true);

      const { status } = await authLogin({
        username: data.username,
        password: data.password,
      });

      if (status === 401) {
        toast.error("El usuario o la contraseña son incorrectos", {
          position: "top-center",
        });
      } else if (status === 200) {
        toast.success("¡Sesión iniciada con éxito!", {
          position: "top-center",
        });
        navigate("/");
      }
    } catch (error) {
      toast.error("Error al iniciar sesión. Por favor, inténtalo de nuevo.", {
        position: "top-center",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden p-0">
        <CardContent className="grid p-0">
          <form className="p-6 md:p-8" onSubmit={handleSubmit(onSubmit)}>
            <FieldGroup>
              <div className="flex flex-col items-center gap-2 text-center mt-2">
                <h1 className="text-2xl font-bold">Bienvenido/a</h1>
                <p className="text-muted-foreground text-balance">
                  Ingresa a tu cuenta para continuar
                </p>
              </div>

              <Field>
                <FieldLabel htmlFor="username">Usuario</FieldLabel>
                <Input
                  id="username"
                  type="text"
                  placeholder="Nombre de usuario"
                  {...register("username")}
                  className={errors.username ? "border-red-500" : ""}
                />
                {errors.username && (
                  <p className="text-red-500 text-sm">
                    <CircleX className="inline mr-1 h-4 w-4" />
                    {errors.username.message}
                  </p>
                )}
              </Field>

              <Field>
                <div className="flex items-center">
                  <FieldLabel htmlFor="password">Contraseña</FieldLabel>
                </div>
                <Input
                  id="password"
                  type="password"
                  placeholder="***********"
                  {...register("password")}
                  className={errors.password ? "border-red-500" : ""}
                />
                {errors.password && (
                  <p className="text-red-500 text-sm">
                    <CircleX className="inline mr-1 h-4 w-4" />
                    {errors.password.message}
                  </p>
                )}
              </Field>

              <Field>
                <Button type="submit" disabled={isLoading}>
                  {isLoading ? (
                    <>
                      <Spinner />
                      <span>Iniciando sesión...</span>
                    </>
                  ) : (
                    "Iniciar sesión"
                  )}
                </Button>
              </Field>

              <FieldSeparator className="*:data-[slot=field-separator-content]:bg-card" />

              <FieldDescription className="text-center">
                No tienes una cuenta? <Link to="/register">Regístrate</Link>
              </FieldDescription>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>

      <FieldDescription className="px-6 text-center">
        Al hacer clic en continuar, aceptas nuestros{" "}
        <Link to="#">Términos de Servicio</Link> y{" "}
        <Link to="#">Política de Privacidad</Link>.
      </FieldDescription>
    </div>
  );
}
