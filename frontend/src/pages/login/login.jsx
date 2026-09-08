import { useState } from "react";
import authService from "../../services/authService";
import "./login.css";

function Login({ onSuccess }) {
	const [email, setEmail] = useState("");
	const [senha, setSenha] = useState("");
	const [erro, setErro] = useState("");
	const [carregando, setCarregando] = useState(false);

	async function handleSubmit(event) {
		event.preventDefault();
		setErro("");
		setCarregando(true);

		try {
			const resultado = await authService.login(email, senha);
			onSuccess?.(resultado);
		} catch (error) {
			const mensagem = error.response?.data?.detail;
			setErro(mensagem || "Não foi possível entrar. Tente novamente.");
		} finally {
			setCarregando(false);
		}
	}

	return (
		<main className="login-page">
			<section className="login-container">
				<section className="login-intro" aria-labelledby="login-title">
					<p className="login-eyebrow">Vestigium</p>

					<h1 id="login-title">Investigue com clareza.</h1>

					<p className="login-description">
						Reúna fontes, organize evidências e acompanhe suas investigações em
						um só lugar.
					</p>
				</section>

				<section className="login-panel" aria-label="Formulário de login">
					<div className="login-heading">
						<p className="login-kicker">Acesso</p>

						<h2>Bem-vindo de volta</h2>

						<p>Entre na sua conta para continuar.</p>
					</div>

					<form className="login-form" onSubmit={handleSubmit}>
						<label htmlFor="email">Email</label>

						<input
							id="email"
							name="email"
							type="email"
							autoComplete="email"
							value={email}
							onChange={(event) => setEmail(event.target.value)}
							placeholder="voce@exemplo.com"
							required
						/>

						<div className="login-label-row">
							<label htmlFor="senha">Senha</label>
						</div>

						<input
							id="senha"
							name="senha"
							type="password"
							autoComplete="current-password"
							value={senha}
							onChange={(event) => setSenha(event.target.value)}
							placeholder="Digite sua senha"
							required
						/>

						{/* <div className="login-help-row">
							<button className="login-help" type="button" disabled>
								Esqueceu a senha?
							</button>
						</div> */}

						{erro && (
							<p className="login-error" role="alert">
								{erro}
							</p>
						)}

						<button
							className="login-submit"
							type="submit"
							disabled={carregando}
						>
							{carregando ? "Entrando..." : "Entrar"}
						</button>
					</form>

					<p className="login-footer">
						Ainda não tem uma conta? <a href="/register">Criar conta</a>
					</p>
				</section>
			</section>
		</main>
	);
}

export default Login;