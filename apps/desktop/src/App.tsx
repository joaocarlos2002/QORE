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
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">QORE</div>
        <nav aria-label="Navegação principal">
          {navigation.map((item, index) => (
            <button className={index === 0 ? "nav-item active" : "nav-item"} key={item}>
              {item}
            </button>
          ))}
        </nav>
      </aside>
      <main className="content">
        <header>
          <p className="eyebrow">Question Engine</p>
          <h1>Dashboard</h1>
        </header>
        <section className="empty-state" aria-live="polite">
          <h2>Fundação do aplicativo</h2>
          <p>O QORE está pronto para receber os módulos de gerenciamento.</p>
        </section>
      </main>
    </div>
  );
}
