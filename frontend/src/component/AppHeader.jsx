import React from "react";

export default function Header({ active, onNavigate, onLogout }) {
  return (
    <header className="app-header">
      <h2>School System</h2>

      <nav>
        <div className=".nav-container">

        <button
          className={active === "students" ? "active" : ""}
          onClick={() => onNavigate("students")}
        >
          Students
        </button>

        <button
          className={active === "families" ? "active" : ""}
          onClick={() => onNavigate("families")}
        >
          Families
        </button>

        <button onClick={onLogout}>Logout</button>
        </div>

      </nav>
    </header>
  );
}