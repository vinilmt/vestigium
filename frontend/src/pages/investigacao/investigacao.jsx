import { useNavigate } from "react-router-dom";
import authService from "../../services/authService";
import "./investigacao.css";

function Investigacao() {
	const navigate = useNavigate();

	async function handleLogout() {
		try {
			authService.logout();
			navigate("/login");
		} catch (error) {
			console.error("Erro ao encerrar sessão:", error);
		}
	}

	return (
		<main className="investigacao-page">
			<header className="investigacao-header">
				<h1>Criar investigação</h1>

				<button
					className="logout-button"
					type="button"
					onClick={handleLogout}
				>
					Sair
				</button>
			</header>

			<p>tela de investigação</p>
		</main>
	);
}

export default Investigacao;
