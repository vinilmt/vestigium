import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import authService from "../../services/authService";
import "./register.css";

function Register() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmacao, setConfirmacao] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setErro("");

    if (senha !== confirmacao) {
      setErro("As senhas não coincidem.");
      return;
    }

    setCarregando(true);

    try {
      await authService.register(email, senha);
      navigate("/login");
    } catch (error) {
      const mensagem = error.response?.data?.detail;
      setErro(mensagem || "Não foi possível criar a conta. Tente novamente.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <main className="register-page">
      <section className="register-container">
        <section className="register-intro" aria-labelledby="register-title">
          <p className="register-eyebrow">Vestigium</p>
          <h1 id="register-title">Comece sua investigação.</h1>
          <p className="register-description">
            Crie sua conta para guardar fontes, evidências e descobertas com
            organização.
          </p>
        </section>

        <section className="register-panel" aria-label="Formulário de registro">
          <div className="register-heading">
            <p className="register-kicker">Novo acesso</p>
            <h2>Criar sua conta</h2>
            <p>Preencha seus dados para começar.</p>
          </div>

          <form className="register-form" onSubmit={handleSubmit}>
          <label htmlFor="register-email">Email</label>
          <input
            id="register-email"
            name="email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="voce@exemplo.com"
            required
          />

          <label htmlFor="register-senha">Senha</label>
          <input
            id="register-senha"
            name="senha"
            type="password"
            autoComplete="new-password"
            value={senha}
            onChange={(event) => setSenha(event.target.value)}
            placeholder="Crie uma senha"
            minLength={6}
            required
          />

          <label htmlFor="register-confirmacao">Confirmar senha</label>
          <input
            id="register-confirmacao"
            name="confirmacao"
            type="password"
            autoComplete="new-password"
            value={confirmacao}
            onChange={(event) => setConfirmacao(event.target.value)}
            placeholder="Repita sua senha"
            minLength={6}
            required
          />

          {erro && (
            <p className="register-error" role="alert">
              {erro}
            </p>
          )}

          <button className="register-submit" type="submit" disabled={carregando}>
            {carregando ? "Criando conta..." : "Criar conta"}
          </button>
          </form>

          <p className="register-footer">
            Já tem uma conta? <Link to="/login">Entrar</Link>
          </p>
        </section>
      </section>
    </main>
  );
}

export default Register;