import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getCweDetails } from "../components/apis";

const FindingPage = () => {
  const location = useLocation();
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

  if (!data) return <p>Loading...</p>;

  return (
    <div className="page">
      <h2>CWE-{cweId}</h2>
      <h4>Source Table: {table}</h4>

      <table>
        <tbody>
          {Object.entries(data).map(([key, value]) => (
            <tr key={key}>
              <td><b>{key}</b></td>
              <td>{String(value)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FindingPage;
