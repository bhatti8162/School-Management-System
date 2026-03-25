import React, { useRef, useState, useMemo } from "react";

export default function StudentList({ students, selected, onSelect, onImport, authToken }) {
  const fileInputRef = useRef();
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");

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

  const filteredStudents = useMemo(() => {
    const lower = search.toLowerCase();
    return students.filter(
      (s) =>
        s.name.toLowerCase().includes(lower) ||
        String(s.GR_Id).toLowerCase().includes(lower)
    );
  }, [search, students]);

  return (
    <section className="list-container student-section">
      {/* Header */}
      <div className="list-header">
        <h2>Student Directory</h2>
        <div className="actions button-group">
          <button
            onClick={handleExport}
            disabled={loading}
            className="button button-export"
          >
            {loading ? "Processing..." : "Export CSV"}
          </button>
          <button
            onClick={handleImportClick}
            disabled={loading}
            className="button button-import"
          >
            {loading ? "Processing..." : "Import CSV"}
          </button>
          <input
            type="file"
            ref={fileInputRef}
            accept=".csv"
            style={{ display: "none" }}
            onChange={handleFileChange}
          />
        </div>
      </div>

      {/* Search */}
      <input
        type="text"
        placeholder="Search by name or GR_Id..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="student-search list-search"
      />

      {/* Student Grid */}
      <div className="dashboard-grid student-grid">
        {filteredStudents.map((s) => (
          <div
            key={s.GR_Id}
            onClick={() => onSelect(s)}
            className={`dashboard-card student-card ${selected?.GR_Id === s.GR_Id ? "selected" : ""}`}
          >
            <div className="item-left">
              <h3>{s.name}</h3>
              <p>GR_Id: {s.GR_Id}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}