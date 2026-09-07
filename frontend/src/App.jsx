import { useEffect, useState } from "react";
import investigacaoService from "./services/investigacaoService";

function App() {
  const [investigacoes, setInvestigacoes] = useState([]);

  useEffect(() => {
    investigacaoService
      .listar()
      .then((data) => {
        setInvestigacoes(data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <main>
      <h1>Sistema de Investigação</h1>

      <h2>Investigações</h2>

      <ul>
        {investigacoes.map((investigacao) => (
          <li key={investigacao.id}>
            {investigacao.titulo}
          </li>
        ))}
      </ul>
    </main>
  );
}

export default App;
