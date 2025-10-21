import { types } from "../types";

interface AuthState {
  logged: boolean;
  user: any | null;
}

export const authReducer = (
  state: AuthState = { logged: false, user: null },
  action: any
) => {
  switch (action.type) {
    case types.LOGIN:
      return {
        ...state,
        logged: true,
        user: action.payload,
      };

    case types.LOGOUT:
      return {
        ...state,
        logged: false,
        user: null,
      };

    case types.CHECK_SESSION:
      return {
        ...state,
        logged: true,
        user: action.payload.user,
      };

    default:
      return state;
  }
};
