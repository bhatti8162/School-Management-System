import React, { useRef, useState, useMemo } from "react";
import { FaPlus } from "react-icons/fa"; // plus icon
import FamilyProfile from "./FamilyProfile"; // your existing family form component

export default function FamilyList({ families, selected, onSelect, onImport, authToken }) {
  const fileInputRef = useRef();
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false); // toggle for new family form
  const [newFamily, setNewFamily] = useState(null); // store new family data temporarily

  // --- Auth fetch helper ---
  const fetchWithAuth = (url, options = {}) => {
    const opts = {
      ...options,
      credentials: "include",
      headers: {
        ...options.headers,
        Authorization: authToken ? `Bearer ${authToken}` : undefined,
      },
    };
    return fetch(url, opts);
  };

  // --- Search filtering ---
  const filteredFamilies = useMemo(() => {
    const lower = search.toLowerCase();
    return families.filter(
      (f) =>
        (f.father_name?.toLowerCase().includes(lower) ||
         f.mother_name?.toLowerCase().includes(lower) ||
         f.family_id?.toLowerCase().includes(lower))
    );
  }, [search, families]);

  // --- Handle creating new family ---
  const handleAddFamily = () => {
    setNewFamily({});
    setShowForm(true);
  };

  const handleFormSubmit = async (formData) => {
    try {
      setLoading(true);
      const res = await fetchWithAuth("/api/families/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error("Failed to add family");
      const savedFamily = await res.json();
      onImport && onImport(savedFamily); // update parent list
      setShowForm(false);
    } catch (err) {
      console.error(err);
      alert("Error adding family");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="list-container family-section">
      {/* Header */}
      <div className="list-header">
        <h2 className="list-title">Family Directory</h2>
        <button className="add-family-btn" onClick={handleAddFamily}>
          <FaPlus /> Add Family
        </button>
      </div>

      {/* Search */}
      <input
        type="text"
        placeholder="Search by father, mother, or Family ID..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="family-search list-search"
      />

      {/* Family Grid */}
      <div className="dashboard-grid family-grid">
        {filteredFamilies.map((f) => (
          <div
            key={f.family_id}
            onClick={() => onSelect && onSelect(f)}
            className={`dashboard-card family-card ${selected?.family_id === f.family_id ? "selected" : ""}`}
          >
            <div className="item-left">
              <h3>{f.father_name} & {f.mother_name}</h3>
              <p>Family ID: {f.family_id}</p>
              {f.guardian_name && <p>Guardian: {f.guardian_name} ({f.guardian_relation})</p>}
              {f.emergency_contact && <p>Emergency: {f.emergency_contact}</p>}
            </div>
          </div>
        ))}
        {filteredFamilies.length === 0 && <p className="no-results">No families found.</p>}
      </div>

      {/* New Family Form Modal */}
      {showForm && (
        <FamilyProfile
          form={newFamily}
          handleChangeParent={(updatedForm) => setNewFamily(updatedForm)}
          handleUpdateParent={handleFormSubmit}
          onBack={() => setShowForm(false)}
          token={authToken}
        />
      )}
    </section>
  );
}