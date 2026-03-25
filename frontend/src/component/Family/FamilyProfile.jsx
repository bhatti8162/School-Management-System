import React, { useState, useEffect, useRef } from "react";
import { FaEdit } from "react-icons/fa";
import html2pdf from "html2pdf.js";

export default function FamilyProfile({
  form: initialForm,
  handleChangeParent,
  handleUpdateParent,
  onBack,
  token,
}) {
  const [form, setForm] = useState(initialForm || {});
  const profileRef = useRef();

  // Sync props form changes
  useEffect(() => {
    setForm(initialForm || {});
  }, [initialForm]);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    handleChangeParent?.(name, value);
  };

  // PATCH update
  const handleUpdate = async () => {
    if (!form.family_id) return alert("Missing family ID");

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/family/${form.family_id}/`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(form),
      });

      if (!res.ok) throw new Error("Update failed");

      alert("Family updated successfully!");
      handleUpdateParent?.();
    } catch (err) {
      console.error(err);
      alert("Error updating family profile");
    }
  };

  // Export PDF
  const handleExportPDF = () => {
    if (!profileRef.current) return;

    const clone = profileRef.current.cloneNode(true);

    // remove buttons
    clone.querySelectorAll("button").forEach((btn) => btn.remove());

    // replace inputs with spans
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
      filename: `family_${form.family_id || "profile"}.pdf`,
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

        <button
          onClick={handleExportPDF}
        >
          Export PDF
        </button>
      </div>

      <h2 className="profile-title">Family Profile</h2>

      <form className="profile-details-section">
        <div className="profile-fields">
          {Object.keys(form).map((key) => (
            <div className="profile-field" key={key}>
              <label>{key.replace(/_/g, " ").toUpperCase()}</label>

              <input
                name={key}
                value={form[key] || ""}
                onChange={handleChange}
                disabled={key === "family_id" || key === "school_id"} // lock ID fields
              />
            </div>
          ))}
        </div>

        <div className="profile-actions">
          <button
            type="button"
            className="btn-primary"
            onClick={handleUpdate}
          >
            SAVE CHANGES
          </button>
        </div>
      </form>
    </section>
  );
}