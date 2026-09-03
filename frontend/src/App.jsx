import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.API_URL;

function App() {
  const [investigacoes, setInvestigacoes] = useState([]);

  useEffect(() => {
    axios
      .get(`${API_URL}/investigacoes`)
      .then((response) => {
        setInvestigacoes(response.data);
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
