const navigation = [
  "Dashboard",
  "Questões",
  "Bancas",
  "Concursos",
  "Coletas",
  "Documentos",
  "Classificação",
  "Validação",
  "Configurações",
];

export function App() {
  const [activePage, setActivePage] = useState("Dashboard");

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">QORE</div>
        <nav aria-label="Navegação principal">
          {navigation.map((item, index) => (
            <button
              className={activePage === item ? "nav-item active" : "nav-item"}
              key={item}
              onClick={() => setActivePage(item)}
            >
              {item}
            </button>
          ))}
        </nav>
      </aside>
      <main className="content">
        <header>
          <p className="eyebrow">Question Engine</p>
          {activePage === "Bancas" ? <BoardPage /> : <h1>{activePage}</h1>}
        </header>
        {activePage !== "Bancas" && (
          <section className="empty-state" aria-live="polite">
            <h2>Fundação do aplicativo</h2>
            <p>O QORE está pronto para receber os módulos de gerenciamento.</p>
          </section>
        )}
      </main>
    </div>
  );
}
import { useState } from "react";

import { BoardPage } from "./features/boards/BoardPage";
