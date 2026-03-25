import { useState, useEffect } from "react";
import StudentDashboard from "./component/Student/StudentDashboard";
import FamilyDashboard from "./component/Family/FamilyDashboard";
import AppHeader from "./component/AppHeader";
import LoginForm from "./component/LoginForm";

function App() {
  const [token, setToken] = useState(localStorage.getItem("access") || "");
  const [module, setModule] = useState("students");
  const [credentials, setCredentials] = useState({ username: "", password: "" });

  // --- Login ---
  const handleLogin = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      });
      const data = await res.json();

      if (data.access) {
        // Save tokens
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        setToken(data.access);

        // Fetch school_id separately
        fetchSchoolId(data.access);
      } else {
        alert("Invalid credentials");
      }
    } catch (err) {
      console.error("Login error:", err);
    }
  };

  // --- Fetch school_id ---
  const fetchSchoolId = async (accessToken) => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/school_id/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`,
        },
      });
      const data = await res.json();
      if (data[0].school_id) {
        localStorage.setItem("school_id", data[0].school_id);
      } else {
        console.warn("school_id not returned from API");
      }
    } catch (err) {
      console.error("Error fetching school_id:", err);
    }
  };

  // --- Logout ---
  const handleLogout = () => {
    localStorage.clear(); // clears tokens + school_id
    setToken("");
    setModule("students");
  };

  // --- Refresh token ---
  const refreshToken = async () => {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) return handleLogout();

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

        // Optional: refetch school_id if needed
        if (!localStorage.getItem("school_id")) {
          fetchSchoolId(data.access);
        }
      } else {
        handleLogout();
      }
    } catch (err) {
      console.error("Refresh token error:", err);
      handleLogout();
    }
  };

  // --- Auto-refresh token every 4 minutes ---
  useEffect(() => {
    const interval = setInterval(refreshToken, 4 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  // --- Not logged in ---
  if (!token) {
    return (
      <LoginForm
        credentials={credentials}
        setCredentials={setCredentials}
        onLogin={handleLogin}
      />
    );
  }

  // --- Main App ---
  return (
    <>
      <AppHeader active={module} onNavigate={setModule} onLogout={handleLogout} />
      {module === "students" && <StudentDashboard token={token} />}
      {module === "families" && <FamilyDashboard token={token} />}
    </>
  );
}

export default App;