import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field";

export function RegisterForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden p-0">
        <CardContent className="grid p-0">
          <form className="p-6 md:p-8">
            <FieldGroup>
              <div className="flex flex-col items-center gap-2 text-center mt-2">
                <h1 className="text-2xl font-bold">Crea tu cuenta</h1>
                <p className="text-muted-foreground text-balance">
                  Ingresa tus datos para registrarte
                </p>
              </div>
              <Field>
                <FieldLabel htmlFor="username">Usuario</FieldLabel>
                <Input
                  id="username"
                  type="text"
                  placeholder="Nombre de usuario"
                  required
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="email">Correo electrónico</FieldLabel>
                <Input
                  id="email"
                  type="email"
                  placeholder="Correo electrónico"
                  required
                />
              </Field>
              <Field>
                <div className="flex items-center">
                  <FieldLabel htmlFor="password">Contraseña</FieldLabel>
                </div>
                <Input
                  id="password"
                  type="password"
                  placeholder="***********"
                  required
                />
              </Field>
              <Field>
                <div className="flex items-center">
                  <FieldLabel htmlFor="confirm-password">
                    Confirmar contraseña
                  </FieldLabel>
                </div>
                <Input
                  id="confirm-password"
                  type="password"
                  placeholder="***********"
                  required
                />
              </Field>
              <Field>
                <Button type="submit">Crear cuenta</Button>
              </Field>
              <FieldSeparator className="*:data-[slot=field-separator-content]:bg-card"></FieldSeparator>
              <FieldDescription className="text-center">
                Ya tienes una cuenta? <Link to="/login">Inicia sesión</Link>
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
