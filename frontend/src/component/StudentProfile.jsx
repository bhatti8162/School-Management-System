import React, { useState, useEffect } from "react";

export default function StudentProfile({ form: initialForm, handleChangeParent, onBack, selected }) {
  const [form, setForm] = useState(initialForm || {});

  useEffect(() => {
    setForm(initialForm || {});
  }, [initialForm]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    handleChangeParent?.(name, value);
  };

  const handleUpdate = async () => {
    const token = localStorage.getItem("access") || localStorage.getItem("access_token") || localStorage.getItem("jwt");
    if (!token) return alert("Login required. Please log in again.");

    const payload = { ...form };
    if (!payload.date_of_birth || payload.date_of_birth === "N/A") payload.date_of_birth = null;
    if (!payload.admission_date || payload.admission_date === "N/A") payload.admission_date = null;
    if (!payload.blood_group || payload.blood_group === "N/A") payload.blood_group = null;

    delete payload.photograph;
    delete payload.transfer_certificate;

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/students/${form.GR_Id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      if (!response.ok) alert(`Update failed: ${response.status} ${response.statusText}`);
      else {
        alert("Student updated successfully!");
        handleChangeParent?.("updated", true);
      }
    } catch (error) {
      console.error("PUT failed: ", error);
      alert("Update failed. See console for details.");
    }
  };

  return (
    <section className="student-profile-section">
      <button className="student-profile-button" onClick={onBack}>← Back</button>
      <h2 className="student-profile-title">Student Profile</h2>
      <form className="student-profile-form">
        {selected.photograph && (
          <img
            src={selected.photograph}
            alt={selected.name}
            className="student-profile-img"
          />
        )}
        <div className="student-profile-fields">
          {Object.keys(form).map((key) => (
            key === "photograph" || key === "transfer_certificate" ? null : (
            <div className="student-profile-field" key={key}>
              <label className="student-profile-label">{key.replace("_", " ").toUpperCase()}</label>
              <input
                className="student-profile-input"
                name={key}
                value={form[key] || ""}
                onChange={handleChange}
                disabled={key === "GR_Id"}
              />
            </div>
            )
          ))}
        </div>
        <div className="student-profile-actions">
          <button type="button" className="student-profile-button" onClick={handleUpdate}>SAVE CHANGES</button>
        </div>
      </form>
    </section>
  );
}