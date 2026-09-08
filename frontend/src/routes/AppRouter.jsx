import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import Login from "../pages/login/login";
import Register from "../pages/register/register";
import Investigacao from "../pages/investigacao/investigacao";
import Perfil from "../pages/perfil/perfil";

function RotaProtegida({ children }) {
  return localStorage.getItem("token") ? children : <Navigate to="/login" replace />;
}

function AppRouter() {
  const navigate = useNavigate();

  return (
    <Routes>
      <Route
        path="/login"
        element={<Login onSuccess={() => navigate("/investigacoes")} />}
      />
      <Route path="/register" element={<Register />} />
      <Route
        path="/investigacoes"
        element={
          <RotaProtegida>
            <Investigacao />
          </RotaProtegida>
        }
      />
      <Route
        path="/perfil"
        element={
          <RotaProtegida>
            <Perfil />
          </RotaProtegida>
        }
      />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default AppRouter;