import React, { useEffect, useState } from "react";
import Header from "./Header";
import LoginForm from "./LoginForm";
import StudentList from "./StudentList";
import StudentProfile from "./StudentProfile";

const API_URL = "http://127.0.0.1:8000/api/students/";

export default function Dashboard() {
  const [token, setToken] = useState(localStorage.getItem("access") || "");
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [students, setStudents] = useState([]);
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({});
  const [view, setView] = useState("list");

  // --- Auth / Token handling ---
  const handleLogout = () => {
    localStorage.clear();
    setToken("");
    setStudents([]);
    setSelected(null);
    setView("list");
  };

  const handleLogin = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      });
      const data = await res.json();
      if (data.access) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        setToken(data.access);
        setCredentials({ username: "", password: "" });
      } else {
        alert("Invalid credentials");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const refreshAccessToken = async () => {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) return null;
    try {
      const res = await fetch("http://127.0.0.1:8000/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
      });
      const data = await res.json();
      if (data.access) {
        localStorage.setItem("access", data.access);
        setToken(data.access);
        return data.access;
      }
    } catch (err) {
      console.error(err);
    }
    handleLogout();
    return null;
  };

  // --- Fetch helper with automatic token refresh ---
  const fetchWithAuth = async (url, options = {}) => {
    let access = localStorage.getItem("access");
    let res = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${access}`,
      },
    });

    if (res.status === 401) {
      access = await refreshAccessToken();
      if (!access) return;
      res = await fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${access}`,
        },
      });
    }
    return res.json();
  };

  // --- Load students ---
  const refreshStudents = async () => {
    if (!token) return;
    const data = await fetchWithAuth(API_URL);
    setStudents(data);
  };

  useEffect(() => {
    refreshStudents();
  }, [token]);

  // --- Student selection / profile ---
  const handleSelect = (student) => {
    setSelected(student);
    setForm(student);
    setView("profile"); // switch view
  };

  const handleBack = () => {
    setSelected(null);
    setView("list"); // go back to list
  };

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleUpdate = async () => {
    if (!selected) return;
    const { GR_Id, admission_number, photograph, transfer_certificate, ...payload } = form;
    try {
      await fetchWithAuth(`${API_URL}${selected.GR_Id}/`, {
        method: "PATCH",
        body: JSON.stringify(payload),
        headers: { "Content-Type": "application/json" },
      });
      refreshStudents();
      setView("list");
      setSelected(null);
    } catch (err) {
      console.error("Update failed:", err);
    }
  };

  if (!token) {
    return (
      <LoginForm
        credentials={credentials}
        setCredentials={setCredentials}
        onLogin={handleLogin}
      />
    );
  }

  return (
    <>
      <Header token={token} onLogout={handleLogout} />
      <main>
        <div className="dashboard">
          {view === "list" && (
            <StudentList
              students={students}
              selected={selected}
              onSelect={handleSelect} // use handleSelect to switch view
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
    </>
  );
}