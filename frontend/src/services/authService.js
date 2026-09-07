import api from "./api";

async function register(email, senha) {
  const response = await api.post("/auth/register", {
    email,
    senha,
  });

  return response.data;
}

async function login(email, senha) {
  const response = await api.post("/auth/login", {
    email,
    senha,
  });

  localStorage.setItem("token", response.data.token);

  return response.data;
}

async function getMe() {
  const response = await api.get("/auth/me");

  return response.data;
}

function logout() {
  localStorage.removeItem("token");
}

export default {
  register,
  login,
  getMe,
  logout,
};