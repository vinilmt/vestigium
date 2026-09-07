import api from "./api";

async function listar() {
  const response = await api.get("/investigacoes");

  return response.data;
}

async function buscarPorId(id) {
  const response = await api.get(`/investigacoes/${id}`);

  return response.data;
}

async function criar(dados) {
  const response = await api.post("/investigacoes", dados);

  return response.data;
}

async function atualizar(id, dados) {
  const response = await api.patch(`/investigacoes/${id}`, dados);

  return response.data;
}

async function remover(id) {
  const response = await api.delete(`/investigacoes/${id}`);

  return response.data;
}

export default {
  listar,
  buscarPorId,
  criar,
  atualizar,
  remover,
};