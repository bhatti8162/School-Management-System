import React, { useRef, useState } from "react";

export default function StudentList({ students, selected, onSelect, onImport, authToken }) {
  const fileInputRef = useRef();
  const [loading, setLoading] = useState(false);

  const fetchWithAuth = (url, options = {}) => {
    const opts = {
      ...options,
      credentials: "include",
      headers: {
        ...options.headers,
        Authorization: authToken ? `Bearer ${authToken}` : undefined,
      },
    };
    return fetch(url, opts);
  };

  const handleExport = async () => {
    try {
      setLoading(true);
      const res = await fetchWithAuth("http://127.0.0.1:8000/api/students/export_csv/");
      if (!res.ok) throw new Error("Export failed: " + res.status);
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "students.csv";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Export failed");
    } finally {
      setLoading(false);
    }
  };

  const handleImportClick = () => fileInputRef.current.click();

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await fetchWithAuth("http://127.0.0.1:8000/api/students/import_csv/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.error) {
        alert("Import failed: " + data.error);
      } else {
        alert(`Created: ${data.created}, Updated: ${data.updated}`);
        if (onImport) onImport();
      }
    } catch (err) {
      console.error(err);
      alert("Import failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section>
      <h2>Students</h2>

      {/* Buttons */}
      <div style={{ marginBottom: "10px", display: "flex", gap: "10px" }}>
        <button onClick={handleExport} disabled={loading}>
          {loading ? "Processing..." : "Export CSV"}
        </button>
        <button onClick={handleImportClick} disabled={loading}>
          {loading ? "Processing..." : "Import CSV"}
        </button>
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: "none" }}
          accept=".csv"
          onChange={handleFileChange}
        />
      </div>

      {/* Student list */}
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
           {s.name} - ({s.GR_Id})
        </div>
      ))}
    </section>
  );
}