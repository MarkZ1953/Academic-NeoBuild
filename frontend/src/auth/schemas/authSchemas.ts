import * as yup from "yup";

export const authLoginSchema = yup.object({
  username: yup.string().required("El usuario es obligatorio"),
  password: yup.string().required("La contraseña es obligatoria"),
});

export const authRegisterSchema = yup.object({
  username: yup.string().required("El usuario es obligatorio"),
  email: yup
    .string()
    .email("Debe ser un correo electrónico válido")
    .required("El correo electrónico es obligatorio"),
  password: yup
    .string()
    .min(8, "La contraseña debe tener al menos 8 caracteres")
    .required("La contraseña es obligatoria"),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref("password")], "Las contraseñas deben coincidir")
    .required("La confirmación de la contraseña es obligatoria"),
});
