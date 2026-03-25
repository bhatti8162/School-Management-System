import React, { useState, useEffect } from "react";
import FamilyList from "./FamilyList";
import FamilyProfile from "./FamilyProfile"; // Create similar to StudentProfile
const API_URL = "http://127.0.0.1:8000/api/family/";

export default function FamilyDashboard({ token }) {
  const [families, setFamilies] = useState([]);
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({});
  const [view, setView] = useState("list");
  const [loading, setLoading] = useState(false);

  // --- Fetch with token ---
  const fetchWithAuth = async (url, options = {}) => {
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      console.error("API Error:", res.status);
      return null;
    }
    return res.json();
  };

  // --- Load all families ---
  const refreshFamilies = async () => {
    setLoading(true);
    const data = await fetchWithAuth(API_URL);
    if (Array.isArray(data)) setFamilies(data);
    setLoading(false);
  };

  useEffect(() => {
    refreshFamilies();
  }, [token]);

  // --- Handle family selection ---
  const handleSelect = async (family) => {
    setLoading(true);
    setSelected(family);
    try {
      const data = await fetchWithAuth(`${API_URL}${family.family_id}/`);
      if (data) {
        setForm(data);
        setView("profile");
      }
    } catch (err) {
      console.error("Failed to load family profile:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setSelected(null);
    setForm({});
    setView("list");
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleUpdate = async () => {
    if (!selected) return;

    try {
      const { family_id, ...payload } = form;
      const res = await fetchWithAuth(`${API_URL}${family_id}/`, {
        method: "PATCH",
        body: JSON.stringify(payload),
      });

      if (!res || res.error) throw new Error("Update failed");
      await refreshFamilies();
      setView("list");
      setSelected(null);
      setForm({});
    } catch (err) {
      console.error("Update failed:", err);
    }
  };

  return (
    <div className="dashboard">
      {view === "list" && (
        <FamilyList
          families={families}
          selected={selected}
          onSelect={handleSelect}
          onImport={refreshFamilies}
          authToken={token}
        />
      )}

      {view === "profile" && selected && (
        <FamilyProfile
          form={form}
          handleChange={handleChange}
          handleUpdate={handleUpdate}
          onBack={handleBack}
          selected={selected}
        />
      )}

      {loading && <p>Loading...</p>}
    </div>
  );
}