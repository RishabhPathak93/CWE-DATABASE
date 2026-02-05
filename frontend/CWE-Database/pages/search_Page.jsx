import { useState } from "react";
import { useNavigate } from "react-router-dom";
// Note: Humne styles App.css/index.css mein daale hain, 
// toh extra css file ki zarurat nahi agar tumne wahan copy kar liya hai.

const SearchPage = () => {
  const [cweId, setCweId] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (!cweId.trim()) return;
    navigate(`/tables?cwe=${cweId}`);
  };

  return (
    <div className="page search-center">
      <h2>CWE Search</h2>
      
      <div className="search-box">
        <input
          type="text"
          placeholder="Enter CWE ID (e.g. 89)"
          value={cweId}
          onChange={(e) => setCweId(e.target.value)}
          className="search-input"
        />
        <button className="search-btn" onClick={handleSearch}>
          Search
        </button>
      </div>
    </div>
  );
};

export default SearchPage;