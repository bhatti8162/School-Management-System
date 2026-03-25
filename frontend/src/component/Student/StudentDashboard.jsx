import React, { useEffect, useState } from "react";
import StudentList from "./StudentList";
import StudentProfile from "./StudentProfile";

const API_URL = "http://127.0.0.1:8000/api/students/";

export default function StudentDashboard({ token }) {
  const [students, setStudents] = useState([]);
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({});
  const [view, setView] = useState("list");

  // --- Fetch helper ---
  const fetchWithAuth = async (url, options = {}) => {
    const res = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      console.error("API error:", res.status);
      return null;
    }

    return res.json();
  };

  // --- Load students ---
  const refreshStudents = async () => {
    if (!token) return;
    const data = await fetchWithAuth(API_URL);
    if (data) setStudents(data);
  };

  useEffect(() => {
    refreshStudents();
  }, [token]);

  // --- Student actions ---
  const handleSelect = (student) => {
    setSelected(student);
    setForm(student);
    setView("profile");
  };

  const handleBack = () => {
    setSelected(null);
    setView("list");
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleUpdate = async () => {
    if (!selected) return;

    const {
      GR_Id,
      admission_number,
      photograph,
      transfer_certificate,
      ...payload
    } = form;

    try {
      const res = await fetch(`${API_URL}${selected.GR_Id}/`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Update failed");

      await refreshStudents();
      setView("list");
      setSelected(null);
    } catch (err) {
      console.error("Update failed:", err);
    }
  };

  // --- UI ---
  return (
    <main>
      <div className="dashboard">

        {view === "list" && (
          <StudentList
            students={students}
            selected={selected}
            onSelect={handleSelect}
            onImport={refreshStudents}
            authToken={token}
          />
        )}

        {view === "profile" && selected && (
          <StudentProfile
            form={form}
            handleChange={handleChange}
            handleUpdate={handleUpdate}
            onBack={handleBack}
            selected={selected}
          />
        )}

      </div>
    </main>
  );
}