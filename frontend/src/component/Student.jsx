import React, { useEffect, useState } from "react";
import Header from "./Header";

const API_URL = "http://127.0.0.1:8000/api/students/";

export default function Student() {
  const [token, setToken] = useState(localStorage.getItem("access") || "");
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [students, setStudents] = useState([]);
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({});
  const [view, setView] = useState("list"); // <-- 'list' or 'profile'

  // ===== AUTH =====
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

  // ===== REFRESH TOKEN =====
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

  // ===== FETCH WRAPPER =====
const fetchWithAuth = async (url, options = {}) => {
  let access = localStorage.getItem("access");

  let res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${access}`,
      ...options.headers,
    },
  });

  if (res.status === 401) {
    access = await refreshAccessToken();
    if (!access) return;
    res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access}`,
        ...options.headers,
      },
    });
  }

  return res.json();
};

  // ===== LOAD DATA =====
  useEffect(() => {
    if (!token) return;
    fetchWithAuth(API_URL).then(setStudents);
  }, [token]);

  // ===== ACTIONS =====
  const handleSelect = (student) => {
    setSelected(student);
    setForm(student);
    setView("profile"); // switch to profile view
  };

  const handleBack = () => {
    setSelected(null);
    setView("list"); // back to list
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

const handleUpdate = async () => {
  if (!selected) return;

  // Remove read-only / file fields
  const { GR_Id, admission_number, photograph, transfer_certificate, ...payload } = form;

  try {
    const res = await fetchWithAuth(`${API_URL}${selected.GR_Id}/`, {
      method: "PATCH", // use PATCH to update only the fields you changed
      body: JSON.stringify(payload),
      headers: { "Content-Type": "application/json" },
    });


    // Refresh student list
    const updated = await fetchWithAuth(API_URL);
    setStudents(updated);
    setView("list");
  } catch (err) {
    console.error("Update failed:", err);
  }
};

  // ===== LOGIN UI =====
  if (!token) {
    return (
      <div className="login">
        <form>
          <h2>LOGIN</h2>

          <input
            placeholder="USERNAME"
            value={credentials.username}
            onChange={(e) =>
              setCredentials({ ...credentials, username: e.target.value })
            }
          />

          <input
            type="password"
            placeholder="PASSWORD"
            value={credentials.password}
            onChange={(e) =>
              setCredentials({ ...credentials, password: e.target.value })
            }
          />

          <button type="button" onClick={handleLogin}>
            LOGIN
          </button>
        </form>
      </div>
    );
  }

  // ===== DASHBOARD =====
  return (
    <>
      <Header token={token} onLogout={handleLogout} />

      <main>
        <div className="dashboard">
          {view === "list" && (
            <section>
              <h2>Students</h2>
              {students.map((s) => (
                <div
                  key={s.GR_Id}
                  onClick={() => handleSelect(s)}
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
                      selected?.GR_Id === s.GR_Id
                        ? "#eff6ff"
                        : "var(--color-surface)",
                  }}
                >
                  {s.name} ({s.admission_number})
                </div>
              ))}
            </section>
          )}

          {view === "profile" && selected && (
            <section>
              <button onClick={handleBack} style={{ marginBottom: "10px" }}>
                ← Back
              </button>
              <h2>Student Profile</h2>
              <form>
                {/* Profile Image */}
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

                {/* ==== ALL YOUR FIELDS KEPT INTACT ==== */}
                <div>
                  <label>FAMILY ID</label>
                  <input
                    name="family_id"
                    value={form.family_id || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>SCHOOL ID</label>
                  <input
                    name="school_id"
                    value={form.school_id || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>SCHOOL NAME</label>
                  <input
                    name="school_name"
                    value={form.school_name || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>GR ID</label>
                  <input
                    name="GR_Id"
                    value={form.GR_Id || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>NAME</label>
                  <input
                    name="name"
                    value={form.name || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>GENDER</label>
                  <input
                    name="gender"
                    value={form.gender || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>DATE OF BIRTH</label>
                  <input
                    name="date_of_birth"
                    value={form.date_of_birth || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>BLOOD GROUP</label>
                  <input
                    name="blood_group"
                    value={form.blood_group || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>NATIONALITY</label>
                  <input
                    name="nationality"
                    value={form.nationality || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>RELIGION</label>
                  <input
                    name="religion"
                    value={form.religion || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>ADDRESS</label>
                  <input
                    name="address"
                    value={form.address || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>CITY</label>
                  <input
                    name="city"
                    value={form.city || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>STATE</label>
                  <input
                    name="state"
                    value={form.state || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>COUNTRY</label>
                  <input
                    name="country"
                    value={form.country || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>POSTAL CODE</label>
                  <input
                    name="postal_code"
                    value={form.postal_code || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>ADMISSION NUMBER</label>
                  <input
                    name="admission_number"
                    value={form.admission_number || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>ADMISSION CLASS</label>
                  <input
                    name="admission_class"
                    value={form.admission_class || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>SECTION</label>
                  <input
                    name="section"
                    value={form.section || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>ACADEMIC YEAR</label>
                  <input
                    name="academic_year"
                    value={form.academic_year || ""}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>ADMISSION STATUS</label>
                  <input
                    name="admission_status"
                    value={form.admission_status || ""}
                    onChange={handleChange}
                  />
                </div>

                <pre style={{ flexBasis: "100%" }}></pre>
                <div>
                <button type="button" id="StudentSaveBtn" onClick={handleUpdate}>
                  SAVE CHANGES
                </button>
                </div>
              </form>
            </section>
          )}
        </div>
      </main>
    </>
  );
}