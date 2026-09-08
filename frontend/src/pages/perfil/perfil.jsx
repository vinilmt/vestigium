import { useEffect, useState } from "react";
import authService from "../../services/authService";
import logo from "../../assets/images/logo.png";
import "./perfil.css";

function Perfil() {
	const [usuario, setUsuario] = useState(null);
	const [erro, setErro] = useState("");

	useEffect(() => {
		authService
			.getMe()
			.then(setUsuario)
			.catch(() => setErro("Não foi possível carregar o perfil."));
	}, []);

	function formatarData(data) {
		return new Intl.DateTimeFormat("pt-BR", {
			dateStyle: "long",
		}).format(new Date(data));
	}

	return (
		<main className="perfil-page">
			<section className="perfil-content" aria-labelledby="perfil-title">
				<img className="perfil-logo" src={logo} alt="Vestigium" />
				<p className="perfil-kicker">Vestigium</p>
				<div className="perfil-title-row">
					<h1 id="perfil-title">Seu perfil</h1>
				</div>
				<p className="perfil-description">
					Consulte as informações básicas da sua conta.
				</p>

				{erro && (
					<p className="perfil-error" role="alert">
						{erro}
					</p>
				)}

				{!usuario && !erro && <p className="perfil-status">Carregando perfil...</p>}

				{usuario && (
					<dl className="perfil-data">
						<div>
							<dt>
								<i className="fa-solid fa-envelope" aria-hidden="true" />
								Email
							</dt>
							<dd>{usuario.email}</dd>
						</div>
						<div>
							<dt>
								<i className="fa-solid fa-circle-user" aria-hidden="true" />
								ID do usuário
							</dt>
							<dd>{usuario.id}</dd>
						</div>
						<div>
							<dt>
								<i className="fa-solid fa-calendar-days" aria-hidden="true" />
								Conta criada em
							</dt>
							<dd>{formatarData(usuario.data_criacao)}</dd>
						</div>
					</dl>
				)}
			</section>
		</main>
	);
}

export default Perfil;