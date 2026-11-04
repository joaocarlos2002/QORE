export type Board = {
  id: number;
  name: string;
  created_at: string;
  updated_at: string;
};

type BoardPage = {
  items: Board[];
  total: number;
  offset: number;
  limit: number;
};

const apiBaseUrl = () => window.__QORE_API_BASE_URL__ ?? "http://127.0.0.1:8000";

const requestHeaders = () => {
  const token = window.__QORE_API_TOKEN__;
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export async function listBoards(): Promise<BoardPage> {
  const response = await fetch(`${apiBaseUrl()}/api/v1/boards`, {
    headers: requestHeaders(),
  });
  if (!response.ok) {
    throw new Error("Não foi possível carregar as bancas.");
  }
  return response.json() as Promise<BoardPage>;
}

export async function createBoard(name: string): Promise<Board> {
  const response = await fetch(`${apiBaseUrl()}/api/v1/boards`, {
    method: "POST",
    headers: { ...requestHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!response.ok) {
    throw new Error("Não foi possível criar a banca.");
  }
  return response.json() as Promise<Board>;
}
