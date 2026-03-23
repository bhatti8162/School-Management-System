import React from "react";

export default function StudentList({ students, selected, onSelect }) {
  return (
    <section>
      <h2>Students</h2>
      {students.map((s) => (
        <div
          key={s.GR_Id}
          onClick={() => onSelect(s)}
          style={{
            border:
              selected?.GR_Id === s.GR_Id
                ? "2px solid var(--color-primary)"
                : "1px solid var(--color-border)",
            padding: "10px",
            marginBottom: "5px",
            borderRadius: "8px",
            cursor: "pointer",
            background:
              selected?.GR_Id === s.GR_Id ? "#eff6ff" : "var(--color-surface)",
          }}
        >
          {s.name} ({s.admission_number})
        </div>
      ))}
    </section>
  );
}