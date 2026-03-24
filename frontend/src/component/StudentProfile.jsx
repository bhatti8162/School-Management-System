import React, { useState, useEffect, useRef } from "react";
import { FaEdit } from "react-icons/fa";

export default function StudentProfile({
  form: initialForm,
  handleChangeParent,
  onBack,
  selected,
}) {
  const [form, setForm] = useState(initialForm || {});
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef();

  useEffect(() => {
    setForm(initialForm || {});
    setPreview(null);
  }, [initialForm]);

  // Handle text input
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    handleChangeParent?.(name, value);
  };

  // Handle image selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setForm((prev) => ({ ...prev, photograph: file }));
    setPreview(URL.createObjectURL(file));
  };

  // Update API
  const handleUpdate = async () => {
    const token =
      localStorage.getItem("access") ||
      localStorage.getItem("access_token") ||
      localStorage.getItem("jwt");

    if (!token) return alert("Login required.");

    const formData = new FormData();

    Object.keys(form).forEach((key) => {
      let value = form[key];

      if (value === "N/A" || value === "") value = null;

      if (value !== null && value !== undefined) {
        formData.append(key, value);
      }
    });

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/students/${form.GR_Id}/`,
        {
          method: "PATCH", // safer for file uploads
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.error(data);
        alert(`Update failed: ${response.status}`);
      } else {
        alert("Student updated successfully!");
        handleChangeParent?.("updated", true);
      }
    } catch (error) {
      console.error("PUT failed:", error);
      alert("Update failed.");
    }
  };

  return (
    <section className="student-profile-section">
      <button className="student-profile-button" onClick={onBack}>
        ← Back
      </button>

      <h2 className="student-profile-title">Student Profile</h2>

      <form className="student-profile-form">
        {/* Image Section */}
        <div className="student-profile-image-wrapper">
          <img
            src={
              preview
                ? preview
                : selected?.photograph || "https://via.placeholder.com/150"
            }
            alt="student"
            className="student-profile-img"
          />

          {/* Edit Icon */}
          <button
            type="button"
            className="edit-icon-btn"
            onClick={() => fileInputRef.current.click()}
          >
            <FaEdit />
          </button>

          {/* Hidden File Input */}
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            style={{ display: "none" }}
            onChange={handleFileChange}
          />
        </div>

        {/* Fields */}
        <div className="student-profile-fields">
          {Object.keys(form).map((key) =>
            key === "photograph" || key === "transfer_certificate" ? null : (
              <div className="student-profile-field" key={key}>
                <label className="student-profile-label">
                  {key.replace(/_/g, " ").toUpperCase()}
                </label>

                <input
                  className="student-profile-input"
                  name={key}
                  value={form[key] || ""}
                  onChange={handleChange}
                  disabled={["GR_Id", "school_id"].includes(key)}
                />
              </div>
            )
          )}
        </div>

        {/* Actions */}
        <div className="student-profile-actions">
          <button
            type="button"
            className="student-profile-button"
            onClick={handleUpdate}
          >
            SAVE CHANGES
          </button>
        </div>
      </form>
    </section>
  );
}