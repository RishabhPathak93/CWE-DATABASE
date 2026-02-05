import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { getCweDetails } from "../components/apis";

const FindingPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const params = new URLSearchParams(location.search);

  const cweId = params.get("cwe");
  const table = params.get("table");

  const [data, setData] = useState(null);

  useEffect(() => {
    if (!cweId || !table) return;

    getCweDetails(table, cweId).then((res) => {
      setData(res);
    });
  }, [cweId, table]);

  if (!data) return (
    <div className="page center-content">
      <div className="loader"></div>
      <p>Loading Security Data...</p>
    </div>
  );

  return (
    <div className="detail-container">
      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate(-1)}>
        ← Back to Tables
      </button>

      <div className="detail-header">
        <h2 style={{ textAlign: 'center', width: '100%' }}>CWE-{cweId}</h2>
        <p className="source-text">Source Table: <span>{table}</span></p>
      </div>

      <div className="table-wrapper">
        <table className="data-display-table">
          <tbody>
            {Object.entries(data)
              .filter(([key]) => key.toLowerCase() !== "id") // 'id' ko list se nikal diya
              .map(([key, value]) => (
                <tr key={key} className="detail-row">
                  <td className="key-cell">
                    <b>{key.replace(/_/g, ' ')}</b>
                  </td>
                  <td className="value-cell">
                    {String(value) === "NaN" || !value ? "N/A" : String(value)}
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FindingPage;