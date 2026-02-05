import { useState } from "react";
import { useNavigate } from "react-router-dom";

const SearchPage = () => {
  const [cweId, setCweId] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (!cweId.trim()) return;
    navigate(`/tables?cwe=${cweId}`);
  };

  return (
    <div className="page">
      <h2>CWE Search</h2>

      <input
        type="text"
        placeholder="Enter CWE ID (e.g. 89)"
        value={cweId}
        onChange={(e) => setCweId(e.target.value)}
      />

      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default SearchPage;
