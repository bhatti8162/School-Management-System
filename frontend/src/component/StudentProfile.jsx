import React from "react";

export default function StudentProfile({ form, handleChange, handleUpdate, onBack, selected }) {
  return (
    <section>
      <button onClick={onBack} style={{ marginBottom: "10px" }}>
        ← Back
      </button>
      <h2>Student Profile</h2>
      <form>
        {selected.photograph && (
          <img
            src={selected.photograph}
            alt={selected.name}
            style={{
              width: "160px",
              height: "160px",
              borderRadius: "50%",
              objectFit: "cover",
              border: "2px solid var(--color-primary)",
              boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
            }}
          />
        )}

        <pre style={{ flexBasis: "100%" }}></pre>

        {Object.keys(form).map((key) => (
          <div key={key}>
            <label>{key.replace("_", " ").toUpperCase()}</label>
            <input
              name={key}
              value={form[key] || ""}
              onChange={handleChange}
              disabled={key === "GR_Id"} // GR_Id is read-only
            />
          </div>
        ))}

        <pre style={{ flexBasis: "100%" }}></pre>
        <div>
          <button type="button" id="StudentSaveBtn" onClick={handleUpdate}>
            SAVE CHANGES
          </button>
        </div>
      </form>
    </section>
  );
}