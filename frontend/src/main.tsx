import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  return (
    <main className="shell">
      <p className="eyebrow">OFFLINE-FIRST / LOCAL GEMMA 4</p>
      <h1>RescueBridge AI</h1>
      <p className="notice">
        Prototype decision support. AI output is unverified. Do not use for emergency dispatch or
        structural safety assessment.
      </p>
      <p>Gate 0 scaffold is ready. Local report intake is next.</p>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
