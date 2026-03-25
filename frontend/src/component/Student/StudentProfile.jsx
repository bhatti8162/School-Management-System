import React, { useState, useEffect, useRef } from "react";
import { FaEdit } from "react-icons/fa";
import html2pdf from "html2pdf.js";

export default function StudentProfile({
  form: initialForm,
  handleChangeParent,
  onBack,
  selected,
}) {
  const [form, setForm] = useState(initialForm || {});
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef();
  const profileRef = useRef();
  const fileRef = useRef(null);

  useEffect(() => {
    setForm(initialForm || {});
    setPreview(null);
    fileRef.current = null;
  }, [initialForm]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    handleChangeParent?.(name, value);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    fileRef.current = file;
    setPreview(URL.createObjectURL(file));
  };

  const handleUpdate = async () => {
    const token =
      localStorage.getItem("access") ||
      localStorage.getItem("access_token") ||
      localStorage.getItem("jwt");
    if (!token) return alert("Login required.");

    const formData = new FormData();
    Object.keys(form).forEach((key) => {
      if (["photograph", "transfer_certificate"].includes(key)) return;
      const value = form[key];
      if (value !== undefined && value !== null && value !== "") {
        formData.append(key, value);
      }
    });
    if (fileRef.current) formData.append("photograph", fileRef.current);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/students/${form.GR_Id}/`,
        {
          method: "PATCH",
          headers: { Authorization: `Bearer ${token}` },
          body: formData,
        }
      );

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        console.error("PATCH error:", data);
        alert(`Update failed: ${response.status}`);
        return;
      }

      alert("Student updated successfully!");
      handleChangeParent?.("updated", true);
      fileRef.current = null;
    } catch (error) {
      console.error("PATCH failed:", error);
      alert("Update failed.");
    }
  };

  const handleExportPDF = () => {
    if (!profileRef.current) return;

    const clone = profileRef.current.cloneNode(true);

    clone.querySelectorAll("button").forEach((btn) => btn.remove());
    clone.querySelectorAll("input").forEach((input) => {
      const span = document.createElement("span");
      span.textContent = input.value;
      span.style.display = "block";
      span.style.fontFamily = "inherit";
      span.style.padding = "4px 0";
      input.parentNode.replaceChild(span, input);
    });

    const opt = {
      margin: 0.3,
      filename: `student_${form.GR_Id || "profile"}.pdf`,
      image: { type: "jpeg", quality: 1 },
      html2canvas: { scale: 2, useCORS: true },
      jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
    };

    html2pdf().set(opt).from(clone).save();
  };

  return (
    <section className="profile-section" ref={profileRef}>
      <div >
        <button  onClick={onBack}>
          ← Back
        </button>

        <button onClick={handleExportPDF} >
          Export PDF
        </button>
      </div>

      <h2 className="profile-title">Student Profile</h2>

      <form className="profile-details-section">
        <div className="profile-image-section">

          <div className="profile-image">
          <img
            src={
              preview
              ? preview
              : form.photograph || selected?.photograph || "https://via.placeholder.com/150"
            }
            alt="student"
            className="profile-img"
            />

          <button
            type="button"
            className="edit-icon-btn"
            onClick={() => fileInputRef.current.click()}
            >
            <FaEdit />
          </button>
            </div>

          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            style={{ display: "none" }}
            onChange={handleFileChange}
          />
        </div>

        <div className="profile-fields">
          {Object.keys(form).map((key) =>
            ["photograph", "transfer_certificate"].includes(key) ? null : (
              <div className="profile-field" key={key}>
                <label className="profile-label">
                  {key.replace(/_/g, " ").toUpperCase()}
                </label>
                <input
                  className="profile-input"
                  name={key}
                  value={form[key] || ""}
                  onChange={handleChange}
                  disabled={["GR_Id", "school_id"].includes(key)}
                />
              </div>
            )
          )}
        </div>

        <div className="profile-actions">
          <button type="button" className="button btn-primary" onClick={handleUpdate}>
            SAVE CHANGES
          </button>
        </div>
      </form>
    </section>
  );
}