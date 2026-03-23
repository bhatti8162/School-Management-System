import React from "react";

export default function Header({ token, onLogout }) {
  return (
    <header>
      <h3>School Dashboard</h3>

      <div>
        {token ? (
          <button onClick={onLogout}>Logout</button>
        ) : null}
      </div>
    </header>
  );
}