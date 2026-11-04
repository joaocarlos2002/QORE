import { FormEvent, useEffect, useState } from "react";

import { Board, createBoard, listBoards } from "../../services/api";

export function BoardPage() {
  const [boards, setBoards] = useState<Board[]>([]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listBoards()
      .then((page) => setBoards(page.items))
      .catch((cause: Error) => setError(cause.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    try {
      const board = await createBoard(name.trim());
      setBoards((current) => [...current, board].sort((a, b) => a.name.localeCompare(b.name)));
      setName("");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Não foi possível criar a banca.");
    }
  }

  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Cadastros</p>
          <h1>Bancas</h1>
        </div>
        <form className="inline-form" onSubmit={handleSubmit}>
          <label>
            <span className="sr-only">Nome da banca</span>
            <input
              minLength={1}
              onChange={(event) => setName(event.target.value)}
              placeholder="Nome da banca"
              required
              value={name}
            />
          </label>
          <button type="submit">Adicionar</button>
        </form>
      </div>
      {error && <p className="error-message">{error}</p>}
      {loading ? (
        <p>Carregando bancas...</p>
      ) : (
        <ul className="data-list">
          {boards.map((board) => (
            <li key={board.id}>{board.name}</li>
          ))}
          {boards.length === 0 && <li>Nenhuma banca cadastrada.</li>}
        </ul>
      )}
    </section>
  );
}
