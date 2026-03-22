import React, { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000/api/students/";

export default function Home() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [students, setStudents] = useState([]);
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({});

  // --- Login function ---
  const handleLogin = () => {
    fetch("http://127.0.0.1:8000/api/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.access) {
          localStorage.setItem("token", data.access);
          setToken(data.access);
          setCredentials({ username: "", password: "" });
        } else {
          alert("Invalid credentials");
        }
      })
      .catch((err) => console.error(err));
  };

  // --- Logout ---
  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
    setStudents([]);
    setSelected(null);
  };

  // --- Fetch students after login ---
  useEffect(() => {
    if (!token) return;

    fetch(API_URL, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setStudents(data))
      .catch((err) => console.error(err));
  }, [token]);

  // --- Select a student ---
  const handleSelect = (student) => {
    setSelected(student);
    setForm(student);
  };

  // --- Handle form change ---
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // --- Update student ---
  const handleUpdate = () => {
    fetch(`${API_URL}${selected.GR_Id}/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(form),
    })
      .then((res) => res.json())
      .then(() => {
        alert("Updated successfully");
        // Refresh list
        return fetch(API_URL, {
          headers: { Authorization: `Bearer ${token}` },
        })
          .then((res) => res.json())
          .then((data) => {
            setStudents(data);
            setSelected(null);
          });
      })
      .catch((err) => console.error(err));
  };

  // --- If not logged in, show login form ---
  if (!token) {
    return (
      <div style={{ padding: "20px" }}>
        <h2>Login</h2>
        <input
          placeholder="Username"
          value={credentials.username}
          onChange={(e) =>
            setCredentials({ ...credentials, username: e.target.value })
          }
          style={{ display: "block", marginBottom: "10px" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={credentials.password}
          onChange={(e) =>
            setCredentials({ ...credentials, password: e.target.value })
          }
          style={{ display: "block", marginBottom: "10px" }}
        />
        <button
          onClick={handleLogin}
          style={{ padding: "10px 20px", cursor: "pointer" }}
        >
          Login
        </button>
      </div>
    );
  }

  // --- Main dashboard ---
  return (
    <div style={{ display: "flex", gap: "20px", padding: "20px" }}>
      {/* Student List */}
      <div style={{ width: "40%" }}>
        <h2>
          Students{" "}
          <button
            onClick={handleLogout}
            style={{ marginLeft: "10px", cursor: "pointer" }}
          >
            Logout
          </button>
        </h2>
        {students.map((s) => (
          <div
            key={s.GR_Id}
            onClick={() => handleSelect(s)}
            style={{
              border: "1px solid #ccc",
              padding: "10px",
              marginBottom: "5px",
              cursor: "pointer",
            }}
          >
            {s.name} ({s.admission_number})
          </div>
        ))}
      </div>

      {/* Edit Form */}
      <div style={{ width: "60%" }}>
        <h2>Edit Student</h2>
        {selected ? (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "10px",
            }}
          >
            <input
              name="name"
              value={form.name || ""}
              onChange={handleChange}
              placeholder="Name"
            />
            <input
              name="gender"
              value={form.gender || ""}
              onChange={handleChange}
              placeholder="Gender"
            />
            <input
              name="date_of_birth"
              value={form.date_of_birth || ""}
              onChange={handleChange}
              placeholder="DOB"
            />
            <input
              name="nationality"
              value={form.nationality || ""}
              onChange={handleChange}
              placeholder="Nationality"
            />
            <input
              name="religion"
              value={form.religion || ""}
              onChange={handleChange}
              placeholder="Religion"
            />
            <input
              name="address"
              value={form.address || ""}
              onChange={handleChange}
              placeholder="Address"
            />
            <input
              name="city"
              value={form.city || ""}
              onChange={handleChange}
              placeholder="City"
            />
            <input
              name="country"
              value={form.country || ""}
              onChange={handleChange}
              placeholder="Country"
            />
            <input
              name="postal_code"
              value={form.postal_code || ""}
              onChange={handleChange}
              placeholder="Postal Code"
            />
            <input
              name="admission_number"
              value={form.admission_number || ""}
              onChange={handleChange}
              placeholder="Admission #"
            />
            <input
              name="admission_class"
              value={form.admission_class || ""}
              onChange={handleChange}
              placeholder="Class"
            />
            <input
              name="section"
              value={form.section || ""}
              onChange={handleChange}
              placeholder="Section"
            />

            <button
              onClick={handleUpdate}
              style={{
                gridColumn: "span 2",
                padding: "10px",
                background: "black",
                color: "white",
                cursor: "pointer",
              }}
            >
              Save Changes
            </button>
          </div>
        ) : (
          <p>Select a student to edit</p>
        )}
      </div>
    </div>
  );
}